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
    
    # Get the last AI message (the reply we just generated)
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[-1], AIMessage):
        logger.error("DECISION_NODE: No AI reply found to analyze")
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
    
    last_ai_reply = messages[-1].content
    
    # Get last user message
    user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    last_user_msg = user_messages[-1].content.lower() if user_messages else ""
    
    # Check if we're in the last section (invest_plan)
    is_last_section = current_section == SectionID.INVEST_PLAN if hasattr(current_section, 'value') else str(current_section) == "invest_plan"
    
    # Enhanced satisfaction detection
    satisfaction_words = ["yes", "good", "great", "perfect", "continue", "next", "satisfied", "looks good", "right", "proceed", "done", "finished", "complete", "that's good", "that is good", "sounds good"]
    is_satisfied = any(word in last_user_msg for word in satisfaction_words) if last_user_msg else None
    
    # Special handling for completion signals
    completion_words = ["satisfied", "done", "finished", "complete", "good", "right", "yes", "that's good", "that is good", "sounds good", "looks good"]
    is_completion_signal = any(word in last_user_msg for word in completion_words) if last_user_msg else False
    
    # Check if Agent has presented a summary in the last reply
    # This ensures we only move to next section after Agent has summarized current section
    summary_indicators = [
        "summary", "summarize", "let's summarize", "here's what", "here is what",
        "does this capture", "does this feel right", "anything you'd like to adjust",
        "anything you'd like to change", "satisfied", "accurate"
    ]
    agent_presented_summary = any(indicator in last_ai_reply.lower() for indicator in summary_indicators)
    
    # Check if current section is marked as DONE
    current_section_id = current_section.value if hasattr(current_section, 'value') else str(current_section)
    section_states = state.get("section_states", {})
    current_section_state = section_states.get(current_section_id) if section_states else None
    current_section_done = (
        current_section_state is not None and 
        hasattr(current_section_state, 'status') and
        current_section_state.status == SectionStatus.DONE
    )
    
    # Determine router directive
    # IMPORTANT: If business plan has been generated, always allow conversation to continue
    if state.get("business_plan"):
        # Business plan already generated - allow user to continue conversation
        router_directive = RouterDirective.STAY
        logger.info("Business plan already generated - allowing conversation to continue")
    elif is_last_section and is_completion_signal:
        router_directive = RouterDirective.STAY  # Stay to allow business plan generation
    elif is_satisfied and (agent_presented_summary or current_section_done):
        # Only move to next section if:
        # 1. User is satisfied AND
        # 2. Agent has presented a summary OR section is already marked as DONE
        router_directive = RouterDirective.NEXT
        logger.info(f"Moving to next section: summary_presented={agent_presented_summary}, section_done={current_section_done}")
    elif is_satisfied and not agent_presented_summary and not current_section_done:
        # User is satisfied but Agent hasn't summarized yet - stay and let Agent summarize
        router_directive = RouterDirective.STAY
        logger.info("User satisfied but no summary yet - staying to allow Agent to summarize")
    else:
        router_directive = RouterDirective.STAY
    
    # Check if we should save content
    # Save when user seems satisfied or when presenting summary
    should_save_content = is_satisfied is True or "summary" in last_ai_reply.lower()
    
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

