# Personal Chief

An AI-powered personal chef built with LangGraph and FastAPI. Snap a photo of your ingredients or type a list — the agent searches the web for recipes, scores them by nutrition and difficulty, and streams back structured recommendations.

## How It Works

1. **Identify** — Recognizes ingredients from uploaded photos (multimodal) or text input
2. **Search** — Queries the web via Tavily to find matching recipes in real time
3. **Score** — Ranks candidates by nutritional value and ease of preparation
4. **Recommend** — Returns a structured report with recipes, scores, and reasoning

## Architecture

```
FastAPI (REST + SSE) ── LangGraph Agent ── Qwen3-Omni-Flash (DashScope)
                              │
                        Tavily Search
                              │
                    SQLite Checkpointer (memory)
```

| Layer | Stack |
|---|---|
| Agent framework | LangGraph + LangChain |
| Model | Qwen3-Omni-Flash (Alibaba DashScope, OpenAI-compatible) |
| Search | Tavily Search API |
| Server | FastAPI + Uvicorn |
| Frontend | Next.js (static export) |
| Storage | SQLite (conversation memory) + Alibaba Cloud OSS (image uploads) |
| Observability | LangSmith Tracing |

## Project Structure

```
app/
  main.py                     FastAPI entry point
  agents/
    personal_chief.py          LangGraph agent definition
  api/v1/
    chat.py                    Chat endpoints (stream, history, clear)
    oss.py                     OSS presigned upload URL
  models/
    schemas.py                 Request / response models
  common/
    logger.py                  Logging configuration
  static/                      Frontend (Next.js static export)
langgraph.json                 LangGraph Studio config
pyproject.toml                 Project metadata and dependencies
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- A [DashScope](https://dashscope.aliyun.com) API key (for Qwen)
- A [Tavily](https://tavily.com) API key (for web search)
- Alibaba Cloud OSS credentials (for image uploads, optional at startup)

### Install

```bash
pip install -e .
```

### Configure

Copy the example below into `.env` and fill in your keys:

```env
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
TAVILY_API_KEY=
OSS_ACCESS_KEY_ID=
OSS_ACCESS_KEY_SECRET=
OSS_BUCKET=
LANGSMITH_TRACING=true          # optional
LANGSMITH_API_KEY=              # optional
LANGSMITH_PROJECT=personal-chief
```

### Run

```bash
python -m app.main
```

On Windows, set `PYTHONUTF8=1` first to avoid encoding issues:

```powershell
$env:PYTHONUTF8=1; python -m app.main
```

Open [http://127.0.0.1:8001](http://127.0.0.1:8001).

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/chat/stream` | Streaming chat (SSE) |
| `GET` | `/api/v1/chat/messages?thread_id=` | Conversation history |
| `DELETE` | `/api/v1/chat/messages?thread_id=` | Clear conversation |
| `GET` | `/api/v1/oss/presign?filename=` | OSS presigned upload URL |

### Chat Request

```json
{
  "message": "What can I cook with these?",
  "image_url": "https://example.com/photo.jpg",
  "thread_id": "session-001"
}
```

`image_url` is optional — omit it for text-only queries.

## Debug with LangGraph Studio

```bash
langgraph dev
```

Then visit [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024).

## License

MIT
