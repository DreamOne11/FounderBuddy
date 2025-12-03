"""Main entrypoint for Founder Buddy Agent."""

import logging
import uuid

from langchain_core.messages import BaseMessage

from .enums import RouterDirective, SectionID
from .graph import build_founder_buddy_graph
from .models import ContextPacket, FounderBuddyData, FounderBuddyState
from .tools import get_context

logger = logging.getLogger(__name__)

# Create the runnable graph
graph = build_founder_buddy_graph()


async def initialize_founder_buddy_state(user_id: int = None, thread_id: str = None) -> FounderBuddyState:
    """Initialize a new Founder Buddy state.
    
    Args:
        user_id: Integer user ID from frontend (will use default if not provided)
        thread_id: Thread UUID (will be generated if not provided)
    """
    
    if not user_id:
        user_id = 1
        logger.info(f"Using default user_id: {user_id}")
    else:
        logger.info(f"Using provided user_id: {user_id}")

    if not thread_id:
        thread_id = str(uuid.uuid4())
        logger.info(f"Generated new thread_id: {thread_id}")
    else:
        try:
            uuid.UUID(thread_id)
        except ValueError:
            thread_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, thread_id))
            logger.info(f"Converted non-UUID thread_id to UUID: {thread_id}")
    
    initial_state = FounderBuddyState(
        user_id=user_id,
        thread_id=thread_id,
        messages=[],
        current_section=SectionID.MISSION,
        router_directive=RouterDirective.NEXT,
    )
    
    # Get initial context for first section
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": SectionID.MISSION.value,
        "founder_data": {},
    })
    
    initial_state["context_packet"] = ContextPacket(**context)
    initial_state["founder_data"] = FounderBuddyData()
    
    logger.info(f"Founder Buddy state initialized with user_id={user_id}, thread_id={thread_id}")
    
    return initial_state


__all__ = [
    "graph",
    "initialize_founder_buddy_state",
]




