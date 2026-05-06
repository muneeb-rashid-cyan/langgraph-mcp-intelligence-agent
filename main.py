from dotenv import load_dotenv
load_dotenv()  # must run before importing agent modules that instantiate LLM clients

import asyncio
from agent.graph import build_graph


async def run(company_name: str) -> None:
    graph = build_graph()

    result = await graph.ainvoke({
        "company_name": company_name,
        "scraped_content": "",
        "stored": False,
        "final_report": "",
        "messages": [],
    })

    print("\n" + "=" * 52)
    print(f"  Intelligence Report: {company_name}")
    print("=" * 52)
    print(result["final_report"])
    print("=" * 52)
    print("→ Report ready.")


if __name__ == "__main__":
    company = input("Enter company name: ").strip()
    if not company:
        print("Error: company name cannot be empty.")
        raise SystemExit(1)
    asyncio.run(run(company))
