"""Initialize node for Concept Pitch Agent."""

import logging
from langchain_core.runnables import RunnableConfig

from ..enums import RouterDirective, SectionID
from ..models import ConceptPitchState

logger = logging.getLogger(__name__)


async def initialize_node(state: ConceptPitchState, config: RunnableConfig) -> ConceptPitchState:
    """Initialize node that ensures all required state fields are present."""
    # Get correct IDs from config
    configurable = config.get("configurable", {})
    
    if "user_id" not in state or not state["user_id"]:
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
        else:
            raise ValueError("Critical system error: No valid user_id found")
    
    # Ensure all required fields have default values
    if "current_section" not in state:
        state["current_section"] = SectionID.SUMMARY_CONFIRMATION
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.STAY  # Stay in summary_confirmation to show Value Canvas data
    
    logger.info(f"Initialized Concept Pitch state for user {state['user_id']}")
    
    return state
