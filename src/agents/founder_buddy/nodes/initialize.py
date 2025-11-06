"""Initialize node for Founder Buddy Agent."""

import logging
from langchain_core.runnables import RunnableConfig

from ..enums import RouterDirective, SectionID
from ..models import FounderBuddyState

logger = logging.getLogger(__name__)


async def initialize_node(state: FounderBuddyState, config: RunnableConfig) -> FounderBuddyState:
    """Initialize node that ensures all required state fields are present."""
    configurable = config.get("configurable", {})
    
    if "user_id" not in state or not state["user_id"]:
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
        else:
            raise ValueError("Critical system error: No valid user_id found")
    
    # Ensure all required fields have default values
    if "current_section" not in state:
        state["current_section"] = SectionID.MISSION
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.NEXT
    
    logger.info(f"Initialized Founder Buddy state for user {state['user_id']}")
    
    return state

