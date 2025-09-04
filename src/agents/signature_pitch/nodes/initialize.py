"""Initialize node for Signature Pitch Agent."""

import logging
import uuid

from langchain_core.runnables import RunnableConfig

from ..enums import RouterDirective, SignaturePitchSectionID
from ..models import SignaturePitchData, SignaturePitchState

logger = logging.getLogger(__name__)


async def initialize_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Initialize node that ensures all required state fields are present.
    This is the first node in the graph to handle LangGraph Studio's incomplete state.
    """
    logger.info("Initialize node - Setting up default values")

    # Get correct IDs from config
    configurable = config.get("configurable", {})
    
    if "user_id" not in state or not state["user_id"]:
        # Try to get user_id from config first
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
            logger.info(f"Initialize node - Got user_id from config: {state['user_id']}")
        else:
            # Fallback for LangGraph Studio (no config provided)
            state["user_id"] = 1
            logger.warning(f"Initialize node - No user_id in config, using default: {state['user_id']}")
            logger.info("This is likely LangGraph Studio mode - using safe defaults")
    
    if "thread_id" not in state or not state["thread_id"]:
        # Try to get thread_id from config
        if "thread_id" in configurable and configurable["thread_id"]:
            state["thread_id"] = configurable["thread_id"]
            logger.info(f"Initialize node - Got thread_id from config: {state['thread_id']}")
        else:
            # Generate a new thread_id for LangGraph Studio
            state["thread_id"] = str(uuid.uuid4())
            logger.warning(f"Initialize node - No thread_id in config, generated: {state['thread_id']}")
            logger.info("This is likely LangGraph Studio mode - using generated thread_id")
    
    # Ensure all required fields have default values
    if "current_section" not in state:
        state["current_section"] = SignaturePitchSectionID.ACTIVE_CHANGE
        
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.NEXT
        
    if "finished" not in state:
        state["finished"] = False
        
    if "canvas_data" not in state:
        state["canvas_data"] = SignaturePitchData()
        
    if "section_states" not in state:
        state["section_states"] = {}
        
    if "short_memory" not in state:
        state["short_memory"] = []
        
    if "awaiting_user_input" not in state:
        state["awaiting_user_input"] = False
        
    if "is_awaiting_rating" not in state:
        state["is_awaiting_rating"] = False
        
    if "error_count" not in state:
        state["error_count"] = 0
    
    logger.info(f"Initialize node - Final user_id: {state['user_id']}, thread_id: {state['thread_id']}")
    return state
