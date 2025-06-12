from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from nova_companion.graph.nodes import (
    router_node,
    context_injection_node,
    conversation_node,
    image_node,
    audio_node
)

from nova_companion.graph.state import AICompanionState


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(AICompanionState)

    graph_builder.add_node("router_node",router_node)
    graph_builder.add_node("context_injection_node", context_injection_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("image_node",image_node)
    graph_builder.add_node("audio_node", audio_node)

    return graph_builder

graph = create_workflow_graph().compile()