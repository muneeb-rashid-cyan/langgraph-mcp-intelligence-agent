# 🧠 MarketPulse AI — Competitive Intelligence Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-green?style=for-the-badge&logo=chainlink&logoColor=white"/>
  <img src="https://img.shields.io/badge/MCP-Custom%20Server-purple?style=for-the-badge&logo=anthropic&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Storage-orange?style=for-the-badge&logo=databricks&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-black?style=for-the-badge&logo=openai&logoColor=white"/>
</p>

<p align="center">
  <b>A competitive intelligence agent that scrapes real company news, stores it in a vector database, and generates structured intelligence reports — powered by a custom MCP server and LangGraph orchestration.</b>
</p>

---


## Skills Demonstrated                                                                                                                                                                                              
  - **Agentic AI Systems** — multi-node LangGraph graph with stateful execution flow                                                                                                                       
  - **Custom MCP Server Development** — built FastMCP server with 3 tools, stdio transport
  - **MCP Client Integration** — connected a LangGraph agent to an external server via the Model Context Protocol                                                                                          
  - **RAG Pipeline** — scrape → embed → store → semantic search → generate                                                                                                                                 
  - **Vector Database** — ChromaDB with metadata filtering and cosine similarity search                                                                                                                    
  - **Async Python** — all agent nodes and MCP client calls are fully async                                                                                                                                
  - **AI Observability** — end-to-end LangSmith tracing across nodes, tools, and LLM calls                                                                                                                 
  - **Protocol Design** — agent communicates with tools over JSON-RPC, not direct function calls

---
## What It Does

Type a company name. Get a structured intelligence report in seconds.

```
Enter company name: Arbisoft

→ Fetching news...
→ Storing intelligence...
→ Analyzing...

====================================================
  Intelligence Report: Arbisoft
====================================================
Key Findings:
Arbisoft has signed an MOU with Thakaat to enhance digital
education aligned with Saudi Vision 2030. Co-founder Yasser
Bashir highlights trust-building with early-stage startups.

Market Position Signal:
Arbisoft is positioning itself as a key player in the digital
education sector within the Saudi market, enhancing credibility
among regional stakeholders.

Recommended Action:
Explore collaboration opportunities with Arbisoft in digital
education and startup incubation to capitalize on the growing
digital transformation landscape in the region.
====================================================
→ Report ready.
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     main.py (CLI)                       │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   LangGraph Agent   │
              │                     │
              │  ┌───────────────┐  │
              │  │ scraper_node  │──┼──► MCP Client ──stdio──► FastMCP Server
              │  └───────┬───────┘  │                          └─► Google News RSS
              │          │          │
              │  ┌───────▼───────┐  │
              │  │ storage_node  │──┼──► MCP Client ──stdio──► FastMCP Server
              │  └───────┬───────┘  │                          └─► ChromaDB
              │          │          │
              │  ┌───────▼───────┐  │
              │  │ analysis_node │──┼──► MCP Client ──stdio──► FastMCP Server
              │  └───────┬───────┘  │                          └─► ChromaDB (search)
              │          │          │                ──────────► GPT-4o-mini
              └──────────┼──────────┘
                         │
                  Final Report + LangSmith Trace
```

> **Key Design**: The MCP server runs as a **separate subprocess**. The agent communicates with it through the MCP protocol over stdio — not direct Python imports. This mirrors exactly how production MCP integrations work.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent Orchestration** | LangGraph | Stateful graph — scraper → storage → analysis |
| **Tool Protocol** | MCP (Model Context Protocol) | Standard interface between agent and tools |
| **MCP Server** | FastMCP | Custom server exposing 3 tools over stdio |
| **News Source** | Google News RSS | Free, no API key required |
| **Vector Storage** | ChromaDB | Local persistent semantic search |
| **LLM** | GPT-4o-mini | Report generation — cost-efficient |
| **Observability** | LangSmith | Full trace of every node, tool call, and LLM call |

---

## Project Structure

```
marketpulse-ai/
├── mcp_servers/
│   └── intelligence_server.py   ← FastMCP server (3 tools, runs as subprocess)
├── agent/
│   ├── graph.py                 ← LangGraph graph definition
│   ├── nodes.py                 ← 3 async nodes, each connects via MCP client
│   └── state.py                 ← AgentState TypedDict
├── vectordb/
│   └── chroma_client.py         ← ChromaDB add + semantic search
├── tools/
│   ├── test_mcp_server.py       ← Test all 3 MCP tools in isolation
│   └── seed_chroma.py           ← Seed ChromaDB with sample data
├── workflows/
│   ├── dev-setup.md             ← Onboarding guide
│   ├── add-mcp-tool.md          ← How to extend the MCP server
│   └── test-mcp-server.md       ← Debugging guide
├── main.py                      ← CLI entry point
├── requirements.txt
└── .env.example                 ← Environment variable template
```

---

## The MCP Pattern (Core Learning)

This project demonstrates the **client-server MCP protocol** end to end.

**Server side** — register a Python function as an MCP tool:
```python
from fastmcp import FastMCP

mcp = FastMCP("intelligence-server")

@mcp.tool()
def scrape_company_news(company_name: str) -> str:
    """Fetch latest 5 headlines from Google News RSS."""
    ...

mcp.run(transport="stdio")
```

**Client side** — call the tool from the LangGraph agent:
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(SERVER_PARAMS) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("scrape_company_news", {"company_name": company})
```

The agent **never imports** the server's Python functions directly. All communication is through the MCP protocol — the same way Claude Desktop and Cursor connect to MCP servers.

---

## Quick Start

### 1. Clone and set up environment
```bash
git clone https://github.com/your-username/marketpulse-ai.git
cd marketpulse-ai

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in:
```
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=marketpulse-ai
LANGCHAIN_TRACING_V2=true
```

> **LangSmith** is free at [smith.langchain.com](https://smith.langchain.com). Traces show every node, MCP tool call, and LLM call.

### 3. Test the MCP server in isolation
```bash
python tools/test_mcp_server.py --company "Apple"
```

Expected:
```
[scrape_company_news] OK — 5 headlines returned
[store_intelligence]  OK — Stored intelligence for Apple at ...
[search_intelligence] OK — 3 results returned

All 3 MCP tools passed.
```

> First run downloads the ChromaDB embedding model (~80MB). Wait for it.

### 4. Run the agent
```bash
python main.py
```

---

## MCP Tools

| Tool | Input | What It Does |
|------|-------|-------------|
| `scrape_company_news` | `company_name` | Fetches top 5 headlines from Google News RSS |
| `store_intelligence` | `company_name`, `content` | Stores in ChromaDB with timestamp metadata |
| `search_intelligence` | `query`, `company_name` | Semantic similarity search, returns top 3 results |

---

## Observability

Every run is fully traced in LangSmith:

- Each LangGraph node execution
- Every MCP tool call (input + output)
- Every LLM call (prompt + response + token usage)

View traces at [smith.langchain.com](https://smith.langchain.com) under the `marketpulse-ai` project.

---

## Extending the Agent

To add a new MCP tool, follow `workflows/add-mcp-tool.md`:

1. Add `@mcp.tool()` function in `mcp_servers/intelligence_server.py`
2. Call it from a new node in `agent/nodes.py`
3. Wire the node into `agent/graph.py`
4. Test with `python tools/test_mcp_server.py`

---

## Notes

- **No paid scraping APIs** — Google News RSS only
- **No cloud vector DB** — ChromaDB runs locally, data persists in `./chroma_data/`
- **ChromaDB is cumulative** — search returns results from all previous runs (by design)
- **Run from project root** — MCP subprocess path resolution depends on it

---

## License

MIT
