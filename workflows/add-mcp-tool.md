# Add a New MCP Tool

Follow this workflow whenever adding a new capability to the intelligence server.

## Steps

### 1. Define the tool in `mcp_servers/intelligence_server.py`
```python
@mcp.tool
def your_tool_name(param: str) -> str:
    """One-line description of what this tool does."""
    # implementation
    return result_as_plain_text
```

Rules:
- Return type must be `str` — format structured data as plain text before returning
- Keep the function under 30 lines — split helper logic into `vectordb/chroma_client.py` if touching ChromaDB
- Never import from `agent/` inside the server — it runs as a separate process

### 2. No server restart needed
The agent spawns a fresh subprocess per node call. Changes take effect on the next `python main.py` run.

### 3. Call the tool from an agent node in `agent/nodes.py`
```python
result = await session.call_tool("your_tool_name", arguments={"param": value})
content = result.content[0].text
```

### 4. Update state if the tool output persists across nodes
Add the new field to `agent/state.py`:
```python
class AgentState(TypedDict):
    your_new_field: str   # add here
```

### 5. Wire a new node into the graph (if needed)
In `agent/graph.py`:
```python
graph.add_node("your_node", your_node_fn)
graph.add_edge("previous_node", "your_node")
graph.add_edge("your_node", "next_node")
```

### 6. Test the tool in isolation before touching the graph
```bash
python tools/test_mcp_server.py --company "Apple"
```
Add a test case for your new tool at the bottom of `tools/test_mcp_server.py`.

## Checklist
- [ ] Tool defined with `@mcp.tool` decorator
- [ ] Return type is `str`
- [ ] Tool tested via `test_mcp_server.py` before wiring into graph
- [ ] State updated if output needs to persist
- [ ] Graph edges updated
- [ ] LangSmith trace shows new tool call after end-to-end run
