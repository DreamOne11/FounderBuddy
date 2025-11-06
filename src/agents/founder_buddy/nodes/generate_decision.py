"""Generate decision node for Founder Buddy Agent."""

import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model

from ..enums import RouterDirective, SectionID, SectionStatus
from ..models import ChatAgentDecision, ChatAgentOutput, FounderBuddyState

logger = logging.getLogger(__name__)


async def generate_decision_node(state: FounderBuddyState, config: RunnableConfig) -> FounderBuddyState:
    """
    Decision generation node that analyzes conversation and produces structured decisions.
    
    Responsibilities:
    - Analyze complete conversation including the just-generated reply
    - Generate structured decision data (router_directive, score, etc.)
    - Update state with agent_output containing complete ChatAgentOutput
    - Set router_directive and other state flags
    """
    context_packet = state.get("context_packet")
    if context_packet and hasattr(context_packet, 'section_id'):
        current_section = context_packet.section_id
        logger.info(f"Generate decision node - Section: {current_section}")
    else:
        current_section = state['current_section']
        logger.info(f"Generate decision node - Section: {current_section} (fallback)")
    
    # Get messages
    messages = state.get("messages", [])
    
    # Get last user message
    user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    last_user_msg = user_messages[-1].content.lower() if user_messages else ""
    
    # Get the last AI message (could be the reply we just generated, or previous one if generate_reply was skipped)
    last_ai_msg = None
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            last_ai_msg = msg
            break
    
    if not last_ai_msg:
        logger.error("DECISION_NODE: No AI message found to analyze")
        default_decision = ChatAgentDecision(
            router_directive="stay",
            user_satisfaction_feedback=None,
            is_satisfied=None,
            should_save_content=False
        )
        state["agent_output"] = ChatAgentOutput(
            reply="",
            **default_decision.model_dump()
        )
        state["router_directive"] = "stay"
        return state
    
    last_ai_reply = last_ai_msg.content
    
    # Check if we're in the last section (invest_plan)
    is_last_section = current_section == SectionID.INVEST_PLAN if hasattr(current_section, 'value') else str(current_section) == "invest_plan"
    
    # Enhanced satisfaction detection
    satisfaction_words = ["yes", "good", "great", "perfect", "continue", "next", "satisfied", "looks good", "right", "proceed", "done", "finished", "complete"]
    is_satisfied = any(word in last_user_msg for word in satisfaction_words) if last_user_msg else None
    
    # Check if AI just showed a summary (looking for summary indicators)
    # Enhanced detection to catch various summary patterns
    ai_reply_lower = last_ai_reply.lower()
    ai_showed_summary = (
        "summary" in ai_reply_lower or 
        "does this feel right" in ai_reply_lower or
        "does this summary" in ai_reply_lower or
        "here's a summary" in ai_reply_lower or
        "here is a summary" in ai_reply_lower or
        "quick summary" in ai_reply_lower or
        "feel right to you" in ai_reply_lower or
        ("investment plan" in ai_reply_lower and ("summary" in ai_reply_lower or "feel right" in ai_reply_lower)) or
        ("funding amount" in ai_reply_lower and "valuation" in ai_reply_lower and "exit strategy" in ai_reply_lower)
    )
    
    # Determine if we should generate business plan
    # Set flag if:
    # 1. We're in the last section
    # 2. AI just showed a summary
    # 3. User confirmed with "yes"
    # Note: We don't check all_complete here because section states may not be updated yet
    # memory_updater will verify all sections are complete before actually generating
    should_generate_business_plan = (
        is_last_section and 
        ai_showed_summary and 
        is_satisfied and 
        not state.get("business_plan")
    )
    
    if should_generate_business_plan:
        logger.info("User confirmed final summary - setting preliminary flag to generate business plan")
        logger.info(f"Conditions: is_last_section={is_last_section}, ai_showed_summary={ai_showed_summary}, is_satisfied={is_satisfied}, business_plan_exists={bool(state.get('business_plan'))}")
        state["should_generate_business_plan"] = True
    else:
        # Reset flag if conditions not met
        logger.debug(f"Not setting business plan flag: is_last_section={is_last_section}, ai_showed_summary={ai_showed_summary}, is_satisfied={is_satisfied}, business_plan_exists={bool(state.get('business_plan'))}")
        state["should_generate_business_plan"] = False
    
    # Determine router directive
    # If we're generating business plan, stay to allow it to happen
    if should_generate_business_plan:
        router_directive = RouterDirective.STAY  # Stay to allow business plan generation
    elif is_last_section and is_satisfied and not ai_showed_summary:
        # In last section, user satisfied but no summary shown yet - stay to show summary
        router_directive = RouterDirective.STAY
    elif is_satisfied:
        router_directive = RouterDirective.NEXT
    else:
        router_directive = RouterDirective.STAY
    
    # Check if we should save content
    # Save when user seems satisfied or when presenting summary
    # If user confirmed summary, we should save and mark section as DONE
    should_save_content = (
        is_satisfied is True or 
        "summary" in last_ai_reply.lower() or 
        "总结" in last_ai_reply or
        (is_last_section and ai_showed_summary and is_satisfied)  # User confirmed final summary
    )
    
    # Log for debugging
    if is_last_section and ai_showed_summary and is_satisfied:
        logger.info(f"User confirmed final summary - should_save_content={should_save_content}, is_satisfied={is_satisfied}")
    
    decision = ChatAgentDecision(
        router_directive=router_directive.value,
        user_satisfaction_feedback=last_user_msg if last_user_msg else None,
        is_satisfied=is_satisfied,
        should_save_content=should_save_content
    )
    
    # Create agent_output
    state["agent_output"] = ChatAgentOutput(
        reply=last_ai_reply,
        **decision.model_dump()
    )
    
    # Update router_directive
    state["router_directive"] = router_directive.value
    
    logger.info(f"Decision: directive={router_directive.value}, satisfied={is_satisfied}, last_section={is_last_section}")
    
    return state

