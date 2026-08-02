# Personal Chief

基于 LangGraph 和 FastAPI 构建的 AI 私人厨师。拍一张食材照片或输入食材清单，智能体会自动搜索食谱、从营养和难度两个维度打分排序，并流式返回推荐结果。

## 工作流程

1. **识别** — 从上传的照片（多模态）或文字中识别可用食材
2. **检索** — 通过 Tavily 搜索引擎实时查找匹配的菜谱
3. **评分** — 从营养价值和制作难度两个维度对候选食谱量化打分
4. **推荐** — 输出结构化的建议报告，包含食谱、得分和推荐理由

## 架构

```
FastAPI (REST + SSE) ── LangGraph Agent ── Qwen3-Omni-Flash (DashScope)
                              │
                        Tavily Search
                              │
                    SQLite Checkpointer (记忆)
```

| 层级 | 技术 |
|---|---|
| Agent 框架 | LangGraph + LangChain |
| 模型 | Qwen3-Omni-Flash（阿里云 DashScope，兼容 OpenAI） |
| 搜索 | Tavily Search API |
| 服务端 | FastAPI + Uvicorn |
| 前端 | Next.js（静态导出） |
| 存储 | SQLite（对话记忆）+ 阿里云 OSS（图片上传） |
| 可观测 | LangSmith Tracing |

## 项目结构

```
app/
  main.py                     FastAPI 入口
  agents/
    personal_chief.py          LangGraph 智能体定义
  api/v1/
    chat.py                    对话接口（流式、历史、清空）
    oss.py                     OSS 预签名上传
  models/
    schemas.py                 请求/响应模型
  common/
    logger.py                  日志配置
  static/                      前端静态文件（Next.js 导出）
langgraph.json                 LangGraph Studio 配置
pyproject.toml                 项目元数据和依赖
```

## 快速开始

### 环境要求

- Python 3.10 及以上
- [DashScope](https://dashscope.aliyun.com) API Key（模型服务）
- [Tavily](https://tavily.com) API Key（网页搜索）
- 阿里云 OSS 凭证（图片上传，启动时可省略）

### 安装

```bash
pip install -e .
```

### 配置

在项目根目录创建 `.env` 文件，填入以下内容：

```env
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
TAVILY_API_KEY=
OSS_ACCESS_KEY_ID=
OSS_ACCESS_KEY_SECRET=
OSS_BUCKET=
LANGSMITH_TRACING=true          # 可选
LANGSMITH_API_KEY=              # 可选
LANGSMITH_PROJECT=personal-chief
```

### 启动

```bash
python -m app.main
```

Windows 下需先设置编码环境变量：

```powershell
$env:PYTHONUTF8=1; python -m app.main
```

访问 [http://127.0.0.1:8001](http://127.0.0.1:8001)。

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/v1/chat/stream` | 流式对话（SSE） |
| `GET` | `/api/v1/chat/messages?thread_id=` | 获取历史消息 |
| `DELETE` | `/api/v1/chat/messages?thread_id=` | 清空会话 |
| `GET` | `/api/v1/oss/presign?filename=` | 获取 OSS 预签名上传 URL |

### 对话请求示例

```json
{
  "message": "这些食材能做什么菜？",
  "image_url": "https://example.com/photo.jpg",
  "thread_id": "session-001"
}
```

`image_url` 为可选字段，不传则仅使用文字输入。

## LangGraph Studio 调试

```bash
langgraph dev
```

访问 [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)。

## License

MIT
