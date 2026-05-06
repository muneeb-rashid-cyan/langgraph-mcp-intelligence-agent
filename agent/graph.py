from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import scraper_node, storage_node, analysis_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("scraper", scraper_node)
    graph.add_node("storage", storage_node)
    graph.add_node("analysis", analysis_node)

    graph.add_edge(START, "scraper")
    graph.add_edge("scraper", "storage")
    graph.add_edge("storage", "analysis")
    graph.add_edge("analysis", END)

    return graph.compile()
