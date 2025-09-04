"""Routing logic for Mission Pitch Agent."""

import logging
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage

from ..enums import RouterDirective
from ..models import MissionPitchState
from ..prompts import get_next_unfinished_section

logger = logging.getLogger(__name__)


def route_decision(state: MissionPitchState) -> Literal["generate_reply", "implementation"] | None:
    """
    Determine the next node to go to based on current state.
    Adapted from value-canvas sophisticated routing logic.
    """
    # 1. All sections complete → Implementation
    if state.get("finished", False):
        logger.info("Graph control - Mission completed, moving to implementation")
        return "implementation"
    
    # Also check if we have no unfinished sections (alternative completion check)
    next_section = get_next_unfinished_section(state.get("section_states", {}))
    if not next_section:
        logger.info("Graph control - No unfinished sections remaining, moving to implementation")
        return "implementation"
    
    # Helper: determine if there's an unresponded user message
    def has_pending_user_input() -> bool:
        msgs = state.get("messages", [])
        if not msgs:
            return False
        last_msg = msgs[-1]
        # If last message is from user, agent hasn't replied yet
        return isinstance(last_msg, HumanMessage)
    
    directive = state.get("router_directive")
    logger.info(f"Graph control - Router directive: {directive}, Has pending input: {has_pending_user_input()}")
    
    # 2. STAY directive - continue on current section
    if directive == RouterDirective.STAY or (isinstance(directive, str) and directive.lower() == "stay"):
        # If the user has replied since last AI message, forward to Generate Reply.
        if has_pending_user_input():
            logger.info("Graph control - User has new input, going to generate_reply")
            return "generate_reply"

        # If AI is still waiting for user response, halt and wait for next run (prevent repeated questions).
        if state.get("awaiting_user_input", False):
            logger.info("Graph control - AI awaiting user input, halting")
            return None

        # Otherwise, halt directly (typically when just initialized).
        logger.info("Graph control - No pending input and not awaiting, halting")
        return None
    
    # 3. NEXT/MODIFY directive - section transition  
    elif directive == RouterDirective.NEXT or (isinstance(directive, str) and directive.startswith("modify:")):
        # For NEXT/MODIFY directives, we need to let the router handle the transition
        # and then ask the first question for the new section
        
        # If there's a pending user input, it means user has acknowledged the transition
        # Let router process the directive and then go to generate_reply for new section
        if has_pending_user_input():
            logger.info("Graph control - Pending user input with NEXT/MODIFY directive, going to generate_reply")
            return "generate_reply"
        
        # If Generate Reply just set NEXT directive but user hasn't responded yet, halt and wait
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], AIMessage):
            logger.info("Graph control - AI just set NEXT/MODIFY, waiting for user response")
            return None
        
        # Default case - go to generate_reply to ask first question of current section
        logger.info("Graph control - NEXT/MODIFY directive, going to generate_reply for new section")
        return "generate_reply"
    
    # 4. Default case - halt to prevent infinite loops
    logger.info("Graph control - Default case, halting to prevent loops")
    return None
