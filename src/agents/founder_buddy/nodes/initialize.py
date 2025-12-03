"""Initialize node for Founder Buddy Agent."""

import logging
from langchain_core.runnables import RunnableConfig

from ..enums import RouterDirective, SectionID
from ..models import FounderBuddyState

logger = logging.getLogger(__name__)


async def initialize_node(state: FounderBuddyState, config: RunnableConfig) -> FounderBuddyState:
    """Initialize node that ensures all required state fields are present."""
    # Handle both dict and RunnableConfig types for config
    if isinstance(config, dict):
        configurable = config.get("configurable", {})
    else:
        configurable = getattr(config, "configurable", {})
    
    # Set user_id from config if not in state
    if "user_id" not in state or not state["user_id"]:
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
        else:
            raise ValueError("Critical system error: No valid user_id found")
    
    # Set thread_id from config if not in state
    if "thread_id" not in state or not state["thread_id"]:
        if "thread_id" in configurable and configurable["thread_id"]:
            state["thread_id"] = configurable["thread_id"]
            logger.info(f"Initialize node - Got thread_id from config: {state['thread_id']}")
        else:
            # Generate a new thread_id if not provided
            import uuid
            state["thread_id"] = str(uuid.uuid4())
            logger.warning(f"Initialize node - No thread_id in config, generated: {state['thread_id']}")
    
    # Ensure all required fields have default values
    if "current_section" not in state:
        state["current_section"] = SectionID.MISSION
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.NEXT
    
    logger.info(f"Initialized Founder Buddy state for user {state['user_id']}, thread {state['thread_id']}")
    
    return state

