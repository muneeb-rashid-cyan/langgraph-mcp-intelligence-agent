"""
Seed ChromaDB with sample intelligence data for development and testing.
Run from project root: python tools/seed_chroma.py [--company NAME] [--inspect]
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SAMPLE_DATA = [
    {
        "company_name": "Apple",
        "content": (
            "Apple launches Vision Pro 2 with improved battery life. "
            "Q3 revenue beats estimates at $98B. "
            "New AI features rolling out to iPhone 16 series."
        ),
    },
    {
        "company_name": "Microsoft",
        "content": (
            "Microsoft Azure revenue up 29% YoY. "
            "Copilot integration expands to all Office 365 tiers. "
            "Partnership with OpenAI extended through 2030."
        ),
    },
    {
        "company_name": "ARAMCO",
        "content": (
            "Saudi Aramco Q2 net income hits $30B. "
            "New LNG expansion project announced. "
            "Aramco signs clean hydrogen deal with Japan."
        ),
    },
]


def seed(company_filter: str | None = None) -> None:
    from vectordb.chroma_client import add_document

    entries = (
        SAMPLE_DATA
        if not company_filter
        else [d for d in SAMPLE_DATA if d["company_name"].lower() == company_filter.lower()]
    )

    if not entries:
        print(f"No sample data found for company: {company_filter}")
        sys.exit(1)

    for entry in entries:
        add_document(
            company_name=entry["company_name"],
            content=entry["content"],
            source="seed_data",
        )
        print(f"Seeded: {entry['company_name']}")

    print(f"\nSeeded {len(entries)} document(s) into ChromaDB.")


def inspect() -> None:
    import chromadb

    client = chromadb.PersistentClient(path="./chroma_data")
    try:
        collection = client.get_collection("intelligence")
        results = collection.get()
        counts: dict[str, int] = {}
        for meta in results["metadatas"]:
            name = meta.get("company_name", "unknown")
            counts[name] = counts.get(name, 0) + 1
        print("ChromaDB document counts:")
        for company, count in sorted(counts.items()):
            print(f"  {company}: {count} document(s)")
        print(f"\nTotal: {sum(counts.values())} document(s)")
    except Exception:
        print("Collection 'intelligence' not found. Run seed first.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed or inspect MarketPulse ChromaDB")
    parser.add_argument("--company", help="Seed only this company (default: all)")
    parser.add_argument("--inspect", action="store_true", help="Show stored document counts")
    args = parser.parse_args()

    if args.inspect:
        inspect()
    else:
        seed(args.company)
