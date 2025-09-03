"""Mission Pitch Agent implementation using modular LangGraph StateGraph."""

import logging
import uuid

from langchain_core.messages import AIMessage

from .models import MissionPitchState, MissionPitchData, ContextPacket
from .enums import MissionSectionID, RouterDirective
from .tools import get_context
from .graph import build_mission_pitch_graph

logger = logging.getLogger(__name__)


# Create the runnable graph using modular builder
graph = build_mission_pitch_graph()


async def initialize_mission_pitch_state(user_id: int = None, thread_id: str | None = None) -> MissionPitchState:
    """
    Initialize a new Mission Pitch state with the given user and thread IDs.
    
    Args:
        user_id: User ID
        thread_id: Thread ID (optional, will be generated if not provided)
    
    Returns:
        Initialized Mission Pitch state
    """
    if not thread_id:
        thread_id = str(uuid.uuid4())
    
    initial_state = MissionPitchState(
        user_id=user_id,
        thread_id=thread_id,
        current_section=MissionSectionID.HIDDEN_THEME,
        router_directive=RouterDirective.NEXT,
        finished=False,
        canvas_data=MissionPitchData(),
        section_states={},
        short_memory=[],
        awaiting_user_input=False,
        is_awaiting_rating=False,
        error_count=0,
        messages=[],
    )
    
    # Get initial context
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": MissionSectionID.HIDDEN_THEME.value,
        "canvas_data": {},
    })
    
    initial_state["context_packet"] = ContextPacket(**context)
    
    # Add welcome message
    welcome_msg = AIMessage(
        content="Welcome! I'm here to help you discover and articulate your Mission Pitch - "
        "a powerful framework that will clarify your purpose and vision. "
        "Let's start by exploring your Hidden Theme."
    )
    initial_state["messages"].append(welcome_msg)
    
    return initial_state


__all__ = ["graph", "initialize_mission_pitch_state"]
