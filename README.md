# 🍳 Personal Chief - 私人厨师智能体

基于 LangGraph + FastAPI 构建的 AI 私人厨师应用。上传食材照片或输入食材清单，智能体自动检索食谱、评估营养价值与制作难度，给出结构化推荐。

## ✨ 功能

- 🔍 **食材识别**：支持上传食材照片（多模态识别）或文字输入食材清单
- 🍽️ **智能食谱检索**：调用 Tavily 搜索引擎实时查找可行菜谱
- 📊 **多维度评分**：从营养价值和制作难度两个维度量化打分排序
- 💬 **流式对话**：SSE 流式输出，实时展示 AI 回复
- 📝 **会话记忆**：基于 SQLite + LangGraph Checkpoint 持久化对话历史
- 📎 **图片上传**：集成阿里云 OSS 预签名上传

## 🛠️ 技术栈

| 层级 | 技术 |
|---|---|
| AI 框架 | LangGraph + LangChain |
| 模型 | 通义千问 Qwen3-Omni-Flash（阿里云 DashScope） |
| 搜索工具 | Tavily Search API |
| Web 框架 | FastAPI + Uvicorn |
| 前端 | Next.js（静态导出） |
| 存储 | SQLite（对话记忆）+ 阿里云 OSS（图片） |
| 监控 | LangSmith Tracing |

## 📁 项目结构

```
├── app/
│   ├── main.py                    # FastAPI 入口
│   ├── agents/
│   │   └── personal_chief.py      # LangGraph 智能体定义
│   ├── api/v1/
│   │   ├── chat.py                # 对话 API 路由
│   │   └── oss.py                 # OSS 上传签名 API
│   ├── models/
│   │   └── schemas.py             # 数据模型
│   ├── common/
│   │   └── logger.py              # 日志配置
│   └── static/                    # 前端静态文件（Next.js 导出）
├── db/                            # SQLite 数据库目录（自动创建）
├── .env                           # 环境变量配置
├── langgraph.json                 # LangGraph Studio 配置
└── pyproject.toml                 # 项目依赖
```

## 🚀 快速开始

### 1. 环境要求

- Python >= 3.10
- Conda（推荐）或 pip

### 2. 创建环境并安装依赖

```bash
# 创建 conda 环境
conda create -n lang python=3.12 -y
conda activate lang

# 安装依赖
pip install -e .
```

### 3. 配置环境变量

编辑 `.env` 文件，填入以下配置：

```env
# 阿里云 DashScope（模型服务）
DASHSCOPE_API_KEY=your_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Tavily 搜索
TAVILY_API_KEY=your_tavily_api_key

# 阿里云 OSS（图片上传）
OSS_ACCESS_KEY_ID=your_oss_access_key_id
OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret
OSS_BUCKET=your_bucket_name

# LangSmith 监控（可选）
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=personal-chief
```

### 4. 创建数据库目录

```bash
mkdir db
```

### 5. 启动服务

**Windows（PowerShell）：**
```powershell
$env:PYTHONUTF8=1; python -m app.main
```

**Windows（CMD）：**
```cmd
set PYTHONUTF8=1 && python -m app.main
```

**macOS / Linux：**
```bash
python -m app.main
```

启动后访问：**http://127.0.0.1:8001**

## 🔌 API 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/v1/chat/stream` | 流式对话（SSE） |
| `GET` | `/api/v1/chat/messages?thread_id=xxx` | 获取历史消息 |
| `DELETE` | `/api/v1/chat/messages?thread_id=xxx` | 清空会话 |
| `GET` | `/api/v1/oss/presign?filename=xxx.png` | 获取 OSS 上传预签名 URL |

## 🧪 LangGraph Studio 调试

调试 Agent 逻辑时可使用 LangGraph Studio：

```bash
$env:PYTHONUTF8=1; langgraph dev
```

访问 https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## ⚠️ 常见问题

### Windows 中文系统编码错误

如果在 Windows 上遇到 `UnicodeDecodeError: 'gbk' codec can't decode...`，有两种解决方式：

1. **启动时加环境变量**：`$env:PYTHONUTF8=1; python -m app.main`
2. **永久设置 conda 环境**：
   ```bash
   conda env config vars set PYTHONUTF8=1 -n lang
   conda deactivate && conda activate lang
   ```

### 数据库文件无法打开

确保项目根目录下存在 `db/` 文件夹：
```bash
mkdir db
```

### OSS 凭证报错

确保 `.env` 中配置了 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET`，OSS 客户端采用懒加载，未调用上传接口时不影响启动。
