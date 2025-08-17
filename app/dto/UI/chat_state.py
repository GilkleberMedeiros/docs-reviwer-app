from typing import TypedDict, Literal


class ChatState(TypedDict):
    label: str
    state: Literal["complete", "running", "error"]
    query_tasks: list[str]
    messages: list[str]
