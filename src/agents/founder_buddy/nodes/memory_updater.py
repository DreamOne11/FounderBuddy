"""Memory updater node for Founder Buddy Agent."""

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

from core.logging_config import get_logger

from ..enums import RouterDirective, SectionID, SectionStatus
from ..models import SectionContent, SectionState, TiptapDocument, TiptapParagraphNode, TiptapTextNode, FounderBuddyState

logger = get_logger(__name__)


async def memory_updater_node(state: FounderBuddyState, config: RunnableConfig) -> FounderBuddyState:
    """
    Memory updater node that persists section states.
    
    Responsibilities:
    - Update section_states with latest content
    - Update founder_data with extracted values
    - Manage short_memory size
    - Generate business plan when all sections are complete
    """
    current_section = state.get('current_section')
    logger.info(f"Memory updater node - Section: {current_section.value if current_section else 'unknown'}")
    
    agent_out = state.get("agent_output")
    
    if not agent_out:
        logger.debug("No agent output to process")
        return state
    
    # Decide status based on satisfaction and directive
    def _status_from_output(is_satisfied, directive):
        """Return status string."""
        if directive == RouterDirective.NEXT:
            return SectionStatus.DONE.value
        if is_satisfied is not None and is_satisfied:
            return SectionStatus.DONE.value
        return SectionStatus.IN_PROGRESS.value

    # Update section state if we should save content
    if agent_out.should_save_content:
        current_section_id = current_section.value if current_section else "unknown"
        logger.info(f"Should save content for section {current_section_id}, is_satisfied={agent_out.is_satisfied}, directive={agent_out.router_directive}")
        
        # Get the last AI message content
        messages = state.get("messages", [])
        last_ai_msg = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                last_ai_msg = msg
                break
        
        if last_ai_msg:
            # Create section content
            plain_text = last_ai_msg.content
            
            # Create simple Tiptap document
            tiptap_doc = TiptapDocument(
                type="doc",
                content=[
                    TiptapParagraphNode(
                        type="paragraph",
                        content=[
                            TiptapTextNode(type="text", text=plain_text)
                        ]
                    )
                ]
            )
            
            section_content = SectionContent(
                content=tiptap_doc,
                plain_text=plain_text
            )
            
            # Update or create section state
            section_states = state.get("section_states", {})
            
            # If user confirmed final summary, force status to DONE
            # Check if this is the last section and user confirmed summary
            is_last_section = current_section == SectionID.INVEST_PLAN if current_section else False
            if is_last_section and agent_out.is_satisfied:
                # Check if the last AI message contains summary indicators
                ai_content = last_ai_msg.content.lower()
                has_summary = (
                    "summary" in ai_content or 
                    "does this feel right" in ai_content or
                    "quick summary" in ai_content
                )
                if has_summary:
                    # Force status to DONE when user confirms final summary
                    logger.info(f"User confirmed final summary - forcing {current_section_id} to DONE")
                    section_status = SectionStatus.DONE
                else:
                    section_status = SectionStatus(_status_from_output(agent_out.is_satisfied, RouterDirective(agent_out.router_directive)))
            else:
                section_status = SectionStatus(_status_from_output(agent_out.is_satisfied, RouterDirective(agent_out.router_directive)))
            
            section_state = SectionState(
                section_id=current_section,
                content=section_content,
                satisfaction_status="satisfied" if agent_out.is_satisfied else None,
                status=section_status
            )
            
            section_states[current_section_id] = section_state
            state["section_states"] = section_states
            
            logger.info(f"Updated section state for {current_section_id} with status {section_state.status.value}")
        else:
            logger.warning(f"No AI message found to save for section {current_section_id}")
    else:
        logger.debug(f"Not saving content for section {current_section.value if current_section else 'unknown'}, should_save_content={agent_out.should_save_content}")
    
    # Check if all sections are complete and generate business plan
    section_states = state.get("section_states", {})
    all_sections = [SectionID.MISSION, SectionID.IDEA, SectionID.TEAM_TRACTION, SectionID.INVEST_PLAN]
    
    # Check completion status
    all_complete = all(
        section_id.value in section_states and 
        section_states[section_id.value].status == SectionStatus.DONE
        for section_id in all_sections
    )
    
    # Also check if we're in the last section and user said they're done
    current_section = state.get('current_section')
    is_last_section = current_section == SectionID.INVEST_PLAN if current_section else False
    
    # Check if user indicated they're satisfied/done
    user_done = False
    messages = state.get("messages", [])
    if messages:
        last_user_msg = None
        for msg in reversed(messages):
            from langchain_core.messages import HumanMessage
            if isinstance(msg, HumanMessage):
                last_user_msg = msg.content.lower() if hasattr(msg, 'content') else ""
                break
        
        done_keywords = ["satisfied", "done", "finished", "complete", "good", "right", "proceed", "think i'm satisfied"]
        user_done = any(keyword in str(last_user_msg) for keyword in done_keywords) if last_user_msg else False
    
    # Check if we should generate business plan (set flag for router to handle)
    # Only generate business plan if:
    # 1. All sections are marked as DONE (including the current one we just saved), AND
    # 2. User has confirmed the final summary (said "yes" after seeing the summary)
    # We check the flag set by generate_decision, and verify all sections are complete
    
    # Check if generate_decision set the flag (user confirmed summary)
    should_generate_from_decision = state.get("should_generate_business_plan", False)
    
    # Re-check all sections completion status (including any updates we just made)
    section_states = state.get("section_states", {})
    all_sections = [SectionID.MISSION, SectionID.IDEA, SectionID.TEAM_TRACTION, SectionID.INVEST_PLAN]
    
    # Check completion status (re-check after potential updates)
    all_complete = all(
        section_id.value in section_states and 
        section_states[section_id.value].status == SectionStatus.DONE
        for section_id in all_sections
    )
    
    # Only set flag if decision node said so AND all sections are complete
    if should_generate_from_decision and all_complete and not state.get("business_plan"):
        logger.info("All sections complete and user confirmed summary - setting flag to generate business plan")
        logger.info(f"Section states: {[(sid.value, state.get('section_states', {}).get(sid.value, {}).get('status', 'NOT_SET')) for sid in all_sections]}")
        state["should_generate_business_plan"] = True
    else:
        logger.info(f"Not generating business plan: should_generate_from_decision={should_generate_from_decision}, all_complete={all_complete}, business_plan_exists={bool(state.get('business_plan'))}")
        logger.info(f"Section states: {[(sid.value, state.get('section_states', {}).get(sid.value, {}).get('status', 'NOT_SET')) for sid in all_sections]}")
        state["should_generate_business_plan"] = False
    
    # Manage short_memory size (keep last 10 messages)
    short_memory = state.get("short_memory", [])
    if len(short_memory) > 10:
        state["short_memory"] = short_memory[-10:]
    
    return state

