# Test MCP Server

## Quick Test (all 3 tools)
```bash
python tools/test_mcp_server.py --company "ARAMCO"
```

Expected output:
```
[scrape_company_news] OK — 5 headlines returned
[store_intelligence]  OK — Stored intelligence for ARAMCO at 2024-...
[search_intelligence] OK — 3 results returned

All 3 MCP tools passed.
```

## Inspect What's Stored in ChromaDB
```bash
python tools/seed_chroma.py --inspect
```

## Manual stdio Test
The MCP server communicates over stdin/stdout via JSON-RPC. To list available tools:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_servers/intelligence_server.py
```

## Debugging Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| `scrape_company_news` returns empty | Google News RSS rate limit | Wait 60s and retry |
| `store_intelligence` hangs (first call) | ChromaDB downloading embedding model | Wait — do not kill |
| `search_intelligence` returns no results | ChromaDB empty | Run `seed_chroma.py` or `store_intelligence` first |
| `FileNotFoundError` on subprocess spawn | Wrong working directory | Run from project root |
| JSON-RPC parse error | Malformed request in manual test | Check quote escaping in shell |

## Test After Each Change
Run the test script after any change to `mcp_servers/intelligence_server.py` or `vectordb/chroma_client.py` before touching the LangGraph agent.
