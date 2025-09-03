"""Graph builder for Signature Pitch Agent."""

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from ..models import SignaturePitchState
from ..nodes import (
    initialize_node,
    router_node,
    chat_agent_node,
    memory_updater_node,
    implementation_node,
)
from .routes import route_decision


def build_signature_pitch_graph():
    """Build the Signature Pitch agent graph."""
    graph = StateGraph(SignaturePitchState)
    
    # Add nodes
    graph.add_node("initialize", initialize_node)
    graph.add_node("router", router_node)
    graph.add_node("chat_agent", chat_agent_node)
    graph.add_node("memory_updater", memory_updater_node)
    graph.add_node("implementation", implementation_node)
    
    # Add edges
    graph.add_edge(START, "initialize")
    graph.add_edge("initialize", "router")
    
    # Router can go to chat agent or implementation
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "chat_agent": "chat_agent",
            "implementation": "implementation",
            "halt": END,
        }
    )
    
    # Chat agent has no tools, goes directly to memory_updater
    graph.add_edge("chat_agent", "memory_updater")
    
    # Memory updater goes back to router
    graph.add_edge("memory_updater", "router")
    
    # Implementation ends the graph
    graph.add_edge("implementation", END)
    
    return graph.compile()
