"""Graph builder for Mission Pitch Agent."""

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from ..models import MissionPitchState
from ..nodes import (
    generate_decision_node,
    generate_reply_node,
    implementation_node,
    initialize_node,
    memory_updater_node,
    router_node,
)
from .routes import route_decision


def build_mission_pitch_graph():
    """Build the Mission Pitch agent graph with dual-node reply generation."""
    graph = StateGraph(MissionPitchState)
    
    # Add nodes
    graph.add_node("initialize", initialize_node)
    graph.add_node("router", router_node)
    graph.add_node("generate_reply", generate_reply_node)
    graph.add_node("generate_decision", generate_decision_node)
    graph.add_node("memory_updater", memory_updater_node)
    graph.add_node("implementation", implementation_node)
    
    # Add edges
    graph.add_edge(START, "initialize")
    graph.add_edge("initialize", "router")
    
    # Router can go to reply generation or implementation
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "generate_reply": "generate_reply",
            "implementation": "implementation",
            None: END,  # Handle the halt condition
        },
    )
    
    # Main processing flow: Reply → Decision → Memory → Router
    graph.add_edge("generate_reply", "generate_decision")
    graph.add_edge("generate_decision", "memory_updater")
    graph.add_edge("memory_updater", "router")
    
    # Implementation ends the graph
    graph.add_edge("implementation", END)
    
    return graph.compile()
