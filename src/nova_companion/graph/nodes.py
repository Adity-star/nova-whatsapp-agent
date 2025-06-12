import os
from uuid import uuid4

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from nova_companion.graph.state import AICompanionState
from nova_companion.graph.utils.chains import get_character_response_chain, get_router_chain

from nova_companion.graph.utils.helper import (
 get_chat_model,
)
from nova_companion.settings import settings


async def riuter_node(state: AICompanionState):
    chain = get_router_chain()
    response = await chain.ainvoke({"message": state["messages"][-settings.ROUTER_MESSAGES_TO_ANALYZE: ]})

    return {"workflow": response.response_type}