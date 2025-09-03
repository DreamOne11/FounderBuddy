"""Graph builder for Mission Pitch Agent."""

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from ..models import MissionPitchState
from ..nodes import (
    initialize_node,
    router_node,
    chat_agent_node,
    memory_updater_node,
    implementation_node,
)
from .routes import route_decision, should_continue


def build_mission_pitch_graph():
    """Build the Mission Pitch agent graph."""
    graph = StateGraph(MissionPitchState)
    
    # Add nodes
    graph.add_node("initialize", initialize_node)
    graph.add_node("router", router_node)
    graph.add_node("chat_agent", chat_agent_node)
    graph.add_node("memory_updater", memory_updater_node)
    graph.add_node("implementation", implementation_node)
    
    # Add edges
    graph.add_edge(START, "initialize")
    graph.add_edge("initialize", "router")
    
    # Router makes decisions about where to go
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "chat_agent": "chat_agent",
            "implementation": "implementation",
            "halt": END,
            END: END,
        }
    )
    
    graph.add_edge("chat_agent", "memory_updater")
    graph.add_conditional_edges(
        "memory_updater",
        should_continue,
        {
            "router": "router",
        }
    )
    graph.add_edge("implementation", END)
    
    return graph.compile()
