"""Router node for Mission Pitch Agent."""

import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from ..models import MissionPitchState, MissionSectionID, RouterDirective, ContextPacket
from ..prompts import get_next_unfinished_section
from ..tools import get_context

logger = logging.getLogger(__name__)


async def router_node(state: MissionPitchState, config: RunnableConfig) -> MissionPitchState:
    """
    Router node that handles navigation and context loading.
    """
    logger.info("Router node - Processing navigation")
    
    # Check if there's a new user message - if so, reset awaiting_user_input
    msgs = state.get("messages", [])
    if msgs and len(msgs) >= 2:
        last_msg = msgs[-1]
        second_last_msg = msgs[-2]
        # If last message is human and second last is AI, user has responded
        if isinstance(last_msg, HumanMessage) and isinstance(second_last_msg, AIMessage):
            state["awaiting_user_input"] = False
            logger.info("Router node - User has responded, reset awaiting_user_input")
    
    directive = state.get("router_directive", RouterDirective.STAY)
    logger.info(f"Router node - Directive: {directive}")
    
    if directive == RouterDirective.STAY:
        # Stay on current section, no context reload needed
        logger.info("Router node - Staying on current section")
        return state
    
    elif directive == RouterDirective.NEXT:
        # Find next unfinished section
        logger.info("Router node - Looking for next unfinished section")
        next_section = get_next_unfinished_section(state.get("section_states", {}))
        
        if next_section:
            logger.info(f"Router node - Moving to next section: {next_section}")
            state["current_section"] = next_section
            
            # Get context for new section
            context = await get_context.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": next_section.value,
                "canvas_data": state["canvas_data"].model_dump() if state.get("canvas_data") else None,
            })
            
            state["context_packet"] = ContextPacket(**context)
            state["router_directive"] = RouterDirective.STAY
            
        else:
            logger.info("Router node - All sections completed, finishing")
            state["finished"] = True
    
    elif directive.startswith("modify:"):
        # Jump to specific section
        section_id = directive.split(":", 1)[1]
        logger.info(f"Router node - Jumping to section: {section_id}")
        
        try:
            new_section = MissionSectionID(section_id)
            state["current_section"] = new_section
            
            # Get context for new section
            context = await get_context.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": section_id,
                "canvas_data": state["canvas_data"].model_dump() if state.get("canvas_data") else None,
            })
            
            state["context_packet"] = ContextPacket(**context)
            state["router_directive"] = RouterDirective.STAY
            
        except ValueError:
            logger.error(f"Router node - Invalid section ID: {section_id}")
            # Stay on current section if invalid
            state["router_directive"] = RouterDirective.STAY
    
    return state
