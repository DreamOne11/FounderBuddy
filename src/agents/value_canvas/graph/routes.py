"""Routing logic for Value Canvas Agent graph."""

from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage

from ..models import ValueCanvasState
from ..enums import RouterDirective


def route_decision(state: ValueCanvasState) -> Literal["implementation", "generate_reply"] | None:
    """Determine the next node to go to based on current state."""
    # 1. All sections complete → Implementation
    if state.get("finished", False):
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
    
    # 2. STAY directive - continue on current section
    if directive == RouterDirective.STAY or (isinstance(directive, str) and directive.lower() == "stay"):
        # If the user has replied since last AI message, forward to Reply Generation.
        if has_pending_user_input():
            return "generate_reply"

        # If AI is still waiting for user response, halt and wait for next run (prevent repeated questions).
        if state.get("awaiting_user_input", False):
            return None  # Halt execution, wait for user input

        # Otherwise, halt directly (typically when just initialized).
        return None  # Halt execution
    
    # 3. NEXT/MODIFY directive - section transition  
    elif directive == RouterDirective.NEXT or (isinstance(directive, str) and directive.startswith("modify:")):
        # For NEXT/MODIFY directives, we need to let the router handle the transition
        # and then ask the first question for the new section
        
        # If there's a pending user input, it means user has acknowledged the transition
        # Let router process the directive and then go to generate_reply for new section
        if has_pending_user_input():
            return "generate_reply"
        
        # If Generate Decision just set NEXT directive but user hasn't responded yet, halt and wait
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], AIMessage):
            return None  # Halt execution, wait for user input
        
        # Default case - go to generate_reply to ask first question of current section
        return "generate_reply"
    
    # 4. Default case - halt to prevent infinite loops
    return None  # Halt execution