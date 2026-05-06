from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    company_name: str
    scraped_content: str
    stored: bool
    final_report: str
    messages: Annotated[list, add_messages]
