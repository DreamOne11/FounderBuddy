"""Signature Pitch Agent implementation using modular LangGraph StateGraph."""

import logging
import uuid

from langchain_core.messages import AIMessage

from .enums import RouterDirective, SignaturePitchSectionID
from .graph import build_signature_pitch_graph
from .models import ContextPacket, SignaturePitchState
from .tools import get_context

logger = logging.getLogger(__name__)


# Create the runnable graph using modular builder
graph = build_signature_pitch_graph()


async def initialize_signature_pitch_state(
    user_id: int = None, thread_id: str = None
) -> SignaturePitchState:
    """Initialize a new Signature Pitch state.

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

    initial_state = SignaturePitchState(
        user_id=user_id,
        thread_id=thread_id,
        messages=[],
        current_section=SignaturePitchSectionID.CLARITY,
        router_directive=RouterDirective.NEXT,  # Start by loading first section
    )

    # Get initial context
    context = await get_context.ainvoke(
        {
            "user_id": user_id,
            "thread_id": thread_id,
            "section_id": SignaturePitchSectionID.CLARITY.value,
            "canvas_data": {},
        }
    )

    initial_state["context_packet"] = ContextPacket(**context)

    # Add welcome message
    welcome_msg = AIMessage(
        content="Welcome! I'm here to help you create your complete Signature Pitch using the CAPSTONE framework - "
        "a proven, eight-step process for building a persuasive pitch that drives audience action. "
        "Let's start with Step 1: CLARITY - defining what you do in a clear, memorable way using Name-Same-Fame components."
    )
    initial_state["messages"].append(welcome_msg)

    return initial_state


__all__ = ["graph", "initialize_signature_pitch_state"]
