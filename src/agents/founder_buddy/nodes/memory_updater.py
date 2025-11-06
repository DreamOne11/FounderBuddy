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
    # Re-check all sections completion status (including any updates we just made)
    section_states = state.get("section_states", {})
    all_sections = [SectionID.MISSION, SectionID.IDEA, SectionID.TEAM_TRACTION, SectionID.INVEST_PLAN]
    
    # Check completion status (re-check after potential updates)
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
        
        done_keywords = ["yes", "satisfied", "done", "finished", "complete", "good", "right", "proceed", "think i'm satisfied", "that's right", "correct"]
        user_done = any(keyword in str(last_user_msg) for keyword in done_keywords) if last_user_msg else False
    
    # Check invest_plan completion status
    invest_plan_done = (
        SectionID.INVEST_PLAN.value in section_states and 
        section_states[SectionID.INVEST_PLAN.value].status == SectionStatus.DONE
    )
    
    # Check if we should generate business plan (set flag for router to handle)
    # Only generate business plan if:
    # 1. All sections are marked as DONE (including the current one we just saved), AND
    # 2. User has confirmed the final summary (said "yes" after seeing the summary)
    # We check the flag set by generate_decision, and verify all sections are complete
    
    # Check if generate_decision set the flag (user confirmed summary)
    should_generate_from_decision = state.get("should_generate_business_plan", False)
    
    # Additional check: if we're in last section, user said yes, and invest_plan is DONE,
    # but other sections might not be marked DONE yet, we should still generate business plan
    # This handles cases where previous sections were completed but not properly saved
    if is_last_section and user_done and invest_plan_done:
        # Check if user confirmed a summary (look for summary in recent AI messages)
        has_summary_confirmation = False
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                ai_content = msg.content.lower()
                if ("summary" in ai_content or "feel right" in ai_content) and \
                   ("investment plan" in ai_content or "funding amount" in ai_content):
                    has_summary_confirmation = True
                    break
            elif isinstance(msg, HumanMessage):
                # Stop at first user message before summary
                break
        
        if has_summary_confirmation:
            logger.info("Detected user confirmation of final summary - setting flag to generate business plan")
            should_generate_from_decision = True
    
    # Emergency fallback: detect duplicate summary pattern and force business plan generation
    # This prevents infinite loops when AI keeps repeating the same summary
    if is_last_section and not should_generate_from_decision and len(messages) >= 4:
        ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
        if len(ai_messages) >= 2:
            last_ai = ai_messages[-1].content.lower()
            second_last_ai = ai_messages[-2].content.lower()
            # Check if last two AI messages are duplicate summaries
            if ("summary" in last_ai or "feel right" in last_ai) and \
               ("summary" in second_last_ai or "feel right" in second_last_ai):
                key_phrases = ["investment plan", "funding amount", "valuation", "exit strategy"]
                shared_phrases = sum(1 for phrase in key_phrases if phrase in last_ai and phrase in second_last_ai)
                if shared_phrases >= 2 and user_done:
                    logger.warning("EMERGENCY: Detected duplicate summary loop - forcing business plan generation")
                    should_generate_from_decision = True
                    # Force invest_plan to DONE if not already
                    if SectionID.INVEST_PLAN.value not in section_states or \
                       section_states[SectionID.INVEST_PLAN.value].status != SectionStatus.DONE:
                        logger.warning("Forcing invest_plan section to DONE to break loop")
                        if SectionID.INVEST_PLAN.value not in section_states:
                            # Create a minimal section state
                            section_states[SectionID.INVEST_PLAN.value] = SectionState(
                                section_id=SectionID.INVEST_PLAN,
                                content=SectionContent(
                                    content=TiptapDocument(
                                        type="doc",
                                        content=[TiptapParagraphNode(
                                            type="paragraph",
                                            content=[TiptapTextNode(type="text", text="Investment plan confirmed by user")]
                                        )]
                                    ),
                                    plain_text="Investment plan confirmed by user"
                                ),
                                status=SectionStatus.DONE
                            )
                            state["section_states"] = section_states
                        else:
                            section_states[SectionID.INVEST_PLAN.value].status = SectionStatus.DONE
                            state["section_states"] = section_states
                        # Re-check all_complete
                        all_complete = all(
                            section_id.value in section_states and 
                            section_states[section_id.value].status == SectionStatus.DONE
                            for section_id in all_sections
                        )
    
    # Only set flag if decision node said so AND (all sections are complete OR emergency fallback triggered)
    # If emergency fallback was triggered, we've already ensured invest_plan is DONE
    # In that case, we should generate business plan even if other sections aren't marked DONE
    # (they were likely completed in conversation but not properly saved)
    should_generate = (
        should_generate_from_decision and 
        (all_complete or (is_last_section and invest_plan_done and user_done)) and 
        not state.get("business_plan")
    )
    
    if should_generate:
        logger.info("All conditions met - setting flag to generate business plan")
        logger.info(f"should_generate_from_decision={should_generate_from_decision}, all_complete={all_complete}, is_last_section={is_last_section}, invest_plan_done={invest_plan_done}, user_done={user_done}")
        logger.info(f"Section states: {[(sid.value, state.get('section_states', {}).get(sid.value, {}).get('status', 'NOT_SET')) for sid in all_sections]}")
        state["should_generate_business_plan"] = True
    else:
        logger.info(f"Not generating business plan: should_generate_from_decision={should_generate_from_decision}, all_complete={all_complete}, is_last_section={is_last_section}, invest_plan_done={invest_plan_done}, user_done={user_done}, business_plan_exists={bool(state.get('business_plan'))}")
        logger.info(f"Section states: {[(sid.value, state.get('section_states', {}).get(sid.value, {}).get('status', 'NOT_SET')) for sid in all_sections]}")
        state["should_generate_business_plan"] = False
    
    # Manage short_memory size (keep last 10 messages)
    short_memory = state.get("short_memory", [])
    if len(short_memory) > 10:
        state["short_memory"] = short_memory[-10:]
    
    return state

