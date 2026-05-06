"""
LangGraph nodes — each node opens its own MCP connection via stdio client.
This is the core learning pattern: agent calls MCP tools through the protocol,
not by importing Python functions directly.
"""

import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from agent.state import AgentState

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["mcp_servers/intelligence_server.py"],
    env={**os.environ},  # pass current env so ChromaDB path and API keys are available
)

llm = ChatOpenAI(model="gpt-4o-mini")


async def _call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Open a stdio MCP connection, call one tool, close the connection."""
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else ""


async def scraper_node(state: AgentState) -> dict:
    print("→ Fetching news...")
    content = await _call_mcp_tool(
        "scrape_company_news",
        {"company_name": state["company_name"]},
    )
    return {"scraped_content": content}


async def storage_node(state: AgentState) -> dict:
    print("→ Storing intelligence...")
    await _call_mcp_tool(
        "store_intelligence",
        {
            "company_name": state["company_name"],
            "content": state["scraped_content"],
        },
    )
    return {"stored": True}


async def analysis_node(state: AgentState) -> dict:
    print("→ Analyzing...")
    context = await _call_mcp_tool(
        "search_intelligence",
        {
            "query": "latest news developments financial market",
            "company_name": state["company_name"],
        },
    )

    messages = [
        SystemMessage(content=(
            "You are a competitive intelligence analyst. "
            "Write a concise intelligence report based on the retrieved news. "
            "Structure it as: Key Findings, Market Position Signal, Recommended Action. "
            "Keep it under 200 words."
        )),
        HumanMessage(content=(
            f"Company: {state['company_name']}\n\n"
            f"Retrieved intelligence:\n{context}"
        )),
    ]

    response = await llm.ainvoke(messages)
    return {"final_report": response.content, "messages": [response]}
