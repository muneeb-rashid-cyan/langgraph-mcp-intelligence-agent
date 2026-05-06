"""
Test all 3 MCP tools by connecting to the intelligence server via stdio client.
Run from project root: python tools/test_mcp_server.py --company "Apple"
"""

import asyncio
import argparse
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["mcp_servers/intelligence_server.py"],
    env=None,
)


async def run_tests(company: str) -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Tool 1: scrape_company_news
            print("[scrape_company_news] calling...")
            result = await session.call_tool("scrape_company_news", {"company_name": company})
            scraped = result.content[0].text if result.content else ""
            if scraped:
                print(f"[scrape_company_news] OK — {len(scraped.splitlines())} lines returned")
            else:
                print("[scrape_company_news] FAIL — empty response")
                sys.exit(1)

            # Tool 2: store_intelligence
            print("[store_intelligence] calling...")
            result = await session.call_tool(
                "store_intelligence", {"company_name": company, "content": scraped}
            )
            confirmation = result.content[0].text if result.content else ""
            if "Stored" in confirmation:
                print(f"[store_intelligence]  OK — {confirmation}")
            else:
                print(f"[store_intelligence]  FAIL — {confirmation}")
                sys.exit(1)

            # Tool 3: search_intelligence
            print("[search_intelligence] calling...")
            result = await session.call_tool(
                "search_intelligence", {"query": "latest news", "company_name": company}
            )
            search_out = result.content[0].text if result.content else ""
            if search_out:
                print(f"[search_intelligence] OK — {len(search_out.splitlines())} lines returned")
            else:
                print("[search_intelligence] FAIL — no results returned")
                sys.exit(1)

    print("\nAll 3 MCP tools passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test MarketPulse MCP server tools")
    parser.add_argument("--company", default="Apple", help="Company name to use in test")
    args = parser.parse_args()
    asyncio.run(run_tests(args.company))
