from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from utils.logger import logging

from nova_companion.graph.edges import select_workflow, should_summarize_conversation
from nova_companion.graph.nodes import (
    audio_node,
    context_injection_node,
    conversation_node,
    image_node,
    memory_extraction_node,
    memory_injection_node,
    router_node,
    summarize_conversation_node,
)
from nova_companion.graph.state import AICompanionState

logging.info("Loaded graph.py")


@lru_cache(maxsize=1)
def create_workflow_graph():
    logging.info("Called create_workflow_graph")
    graph_builder = StateGraph(AICompanionState)

    graph_builder.add_node("router_node", router_node)
    graph_builder.add_node("context_injection_node", context_injection_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("image_node", image_node)
    graph_builder.add_node("audio_node", audio_node)
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)

    # Define the flow of graph
    graph_builder.add_edge(START, "memory_extraction_node")
    # Then determine response type
    graph_builder.add_edge("memory_extraction_node", "router_node")

    # Then inject both context and memories
    graph_builder.add_edge("router_node", "context_injection_node")
    graph_builder.add_edge("context_injection_node", "memory_injection_node")

    # Then proceed to appropriate response node
    graph_builder.add_conditional_edges("memory_injection_node", select_workflow)

    # Check for summarization after any response
    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("image_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("audio_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


graph = create_workflow_graph().compile()
logging.info("Graph compiled and ready")
