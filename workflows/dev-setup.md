# Dev Setup

## Prerequisites
- Python 3.11+
- pip

## Steps

### 1. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Open .env and fill in OPENAI_API_KEY and LANGSMITH_API_KEY
```

### 4. Verify MCP server works
```bash
python tools/test_mcp_server.py --company "Apple"
```
**First run downloads the ChromaDB embedding model (~80MB) — wait for it before declaring failure.**

Expected output:
```
[scrape_company_news] OK — 5 headlines returned
[store_intelligence]  OK — Stored intelligence for Apple at ...
[search_intelligence] OK — 3 results returned

All 3 MCP tools passed.
```

### 5. Seed test data (optional)
```bash
python tools/seed_chroma.py
```

### 6. Run the agent
```bash
python main.py
```

## LangSmith Setup
1. Sign up at [smith.langchain.com](https://smith.langchain.com)
2. Create a project named `marketpulse-ai`
3. Copy the API key into `.env`
4. After running `main.py`, the trace appears in the project automatically — no extra code needed

## Common Setup Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: mcp` | Dependencies not installed | `pip install -r requirements.txt` |
| `FileNotFoundError: mcp_servers/intelligence_server.py` | Not running from project root | `cd` to project root first |
| Empty news results | Google News RSS rate limit | Wait 60s, retry |
| ChromaDB hangs on first store | Downloading embedding model | Wait, do not kill the process |
