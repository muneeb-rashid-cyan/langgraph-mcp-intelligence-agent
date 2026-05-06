# MarketPulse AI

Competitive intelligence agent: LangGraph orchestrates a FastMCP server (stdio transport) that scrapes Google News, stores in ChromaDB, and generates reports via GPT-4o-mini. Primary learning goal is MCP client-server protocol over stdio.

## Commands

```bash
pip install -r requirements.txt       # first-time setup
python main.py                        # run the agent
python tools/test_mcp_server.py --company "Apple"   # test MCP server in isolation
python tools/seed_chroma.py           # seed ChromaDB with sample data
python tools/seed_chroma.py --inspect # view stored document counts
```

## Required Environment Variables

Copy `.env.example` → `.env` and fill in values before running.

```
OPENAI_API_KEY
LANGSMITH_API_KEY
LANGSMITH_PROJECT=marketpulse-ai
LANGCHAIN_TRACING_V2=true
```

## Architecture Constraints

- MCP server runs as a **child subprocess** via stdio — agent nodes connect through `mcp.client.stdio`, never by importing server functions directly
- Always run `python main.py` from the **project root** — MCP subprocess path resolution depends on it
- LLM is fixed to `gpt-4o-mini` — do not change without explicit approval
- News source is **Google News RSS only** — no paid APIs

## Non-obvious Behaviors

- First `store_intelligence` call downloads the ChromaDB embedding model (~80MB) — expect a 30–60s pause
- ChromaDB persists across runs in `./chroma_data/` — `search_intelligence` returns results from previous sessions
- Each agent node opens its own MCP connection and closes it after the tool call — 3 subprocess connections per full run
- LangSmith tracing is automatic via env vars — no instrumentation code needed in nodes

## Verification

MCP tools must be tested through the client (not called as Python functions):
```bash
python tools/test_mcp_server.py --company "ARAMCO"
```
All 3 tools must return OK. Check LangSmith for traces after each agent run.
