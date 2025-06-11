from langgraph.graph import MessagesState


class AICompanionState(MessagesState):

    summary: str
    current_activity: str
    