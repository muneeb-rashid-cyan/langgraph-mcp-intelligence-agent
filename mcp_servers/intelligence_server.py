"""
FastMCP intelligence server — runs as a separate subprocess via stdio transport.
Agent connects to this via MCP client; never import this file directly into the agent.
"""

import sys
import os

# Allow imports from project root when running as a subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import feedparser
from urllib.parse import quote_plus
from datetime import datetime
from fastmcp import FastMCP
from vectordb.chroma_client import add_document, search_documents

feedparser.USER_AGENT = "MarketPulseAI/1.0"

mcp = FastMCP("intelligence-server")


@mcp.tool()
def scrape_company_news(company_name: str) -> str:
    """Fetch the latest 5 news headlines for a company from Google News RSS."""
    url = (
        f"https://news.google.com/rss/search"
        f"?q={quote_plus(company_name)}&hl=en-US&gl=US&ceid=US:en"
    )
    feed = feedparser.parse(url)

    if not feed.entries:
        return f"No news found for {company_name}."

    lines = [f"Latest news for {company_name}:"]
    for entry in feed.entries[:5]:
        lines.append(f"- {entry.title}")
    return "\n".join(lines)


@mcp.tool()
def store_intelligence(company_name: str, content: str) -> str:
    """Store scraped news content in ChromaDB with company metadata."""
    add_document(
        company_name=company_name,
        content=content,
        source="google_news_rss",
    )
    timestamp = datetime.utcnow().isoformat()
    return f"Stored intelligence for {company_name} at {timestamp}."


@mcp.tool()
def search_intelligence(query: str, company_name: str) -> str:
    """Search ChromaDB for relevant stored intelligence about a company."""
    results = search_documents(query=query, company_name=company_name, n_results=3)

    if not results:
        return f"No stored intelligence found for {company_name}."

    formatted = "\n\n".join(f"[{i + 1}] {doc}" for i, doc in enumerate(results))
    return f"Intelligence for {company_name}:\n\n{formatted}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
