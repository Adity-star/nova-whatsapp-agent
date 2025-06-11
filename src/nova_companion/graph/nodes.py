import os
from uuid import uuid4

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from nova_companion.graph.state import AICompanionState



async def conversation_node(state:AICompanionState, config: RunnableConfig):
 l=l