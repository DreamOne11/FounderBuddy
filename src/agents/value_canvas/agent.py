"""Value Canvas Agent implementation using LangGraph StateGraph."""

import logging
import uuid

from .models import ValueCanvasState, ContextPacket
from .enums import SectionID, RouterDirective
from .tools import get_context
from .graph import build_value_canvas_graph

logger = logging.getLogger(__name__)


# Create the runnable graph
graph = build_value_canvas_graph()


# Initialize function for new conversations
async def initialize_value_canvas_state(user_id: int = None, thread_id: str = None) -> ValueCanvasState:
    """Initialize a new Value Canvas state.
    
    Args:
        user_id: Integer user ID from frontend (will use default if not provided)
        thread_id: Thread UUID (will be generated if not provided)
    """
    
    # Use provided integer user_id or default to 1
    if not user_id:
        user_id = 1
        logger.info(f"Using default user_id: {user_id}")
    else:
        logger.info(f"Using provided user_id: {user_id}")

    # Ensure thread_id is a valid UUID string
    if not thread_id:
        thread_id = str(uuid.uuid4())
        logger.info(f"Generated new thread_id: {thread_id}")
    else:
        try:
            uuid.UUID(thread_id)
        except ValueError:
            thread_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, thread_id))
            logger.info(f"Converted non-UUID thread_id to UUID: {thread_id}")
    
    initial_state = ValueCanvasState(
        user_id=user_id,
        thread_id=thread_id,
        messages=[],
        current_section=SectionID.INTERVIEW,
        router_directive=RouterDirective.NEXT,  # Start by loading first section
    )
    
    # Get initial context
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": SectionID.INTERVIEW.value,
        "canvas_data": {},
    })
    
    initial_state["context_packet"] = ContextPacket(**context)
    
    return initial_state


__all__ = ["graph", "initialize_value_canvas_state"]