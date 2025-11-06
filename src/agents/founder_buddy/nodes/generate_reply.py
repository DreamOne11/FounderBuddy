"""Generate reply node for Founder Buddy Agent."""

import logging

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model

from ..enums import SectionStatus
from ..models import FounderBuddyState

logger = logging.getLogger(__name__)


async def generate_reply_node(state: FounderBuddyState, config: RunnableConfig) -> FounderBuddyState:
    """
    Reply generation node that produces streaming conversational responses.
    
    Responsibilities:
    - Generate conversational reply based on context_packet system prompt
    - Support streaming output token by token
    - Add reply to conversation history
    - Update short_memory
    """
    logger.info(f"Generate reply node - Section: {state['current_section']}")
    
    # Check if conversation is finished (business plan generated)
    if state.get("finished", False) or state.get("business_plan"):
        # Check if business plan message already exists in messages
        messages = state.get("messages", [])
        has_business_plan_message = any(
            isinstance(msg, AIMessage) and 
            ("business plan generated" in msg.content.lower() or "🎉" in msg.content)
            for msg in messages
        )
        
        if not has_business_plan_message:
            # Business plan was generated but message not sent yet - send it now
            business_plan = state.get("business_plan", "")
            if business_plan:
                final_message = f"""# 🎉 Business Plan Generated

Thank you for completing all sections! Below is your complete business plan based on our conversation:

---

{business_plan}

---

**Next Steps:**
1. Review this business plan carefully
2. Adjust and refine based on your actual situation
3. Begin executing the action items outlined in the plan

Best of luck with your venture! 🚀"""
                ai_message = AIMessage(content=final_message)
                state["messages"].append(ai_message)
                logger.info("Added business plan message to conversation")
        
        # Generate a polite message informing user that conversation is complete
        completion_message = """Thank you for using Founder Buddy! 

Your business plan has been generated and is available above. If you'd like to start a new conversation or make changes, please start a new thread.

Is there anything else I can help you with regarding your business plan?"""
        
        ai_message = AIMessage(content=completion_message)
        state["messages"].append(ai_message)
        state["awaiting_user_input"] = True
        
        logger.info("Generated completion message for finished conversation")
        return state
    
    # Check if user just confirmed the final summary - skip generating reply
    # Let memory_updater route to business plan generation instead
    messages = state.get("messages", [])
    if messages:
        from ..enums import SectionID
        
        # Find the last user message
        last_user_msg = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_user_msg = msg
                break
        
        if last_user_msg:
            user_content = last_user_msg.content.lower()
            
            # Check if user confirmed summary (expanded list including combinations)
            satisfaction_words = [
                "yes", "good", "great", "perfect", "right", "correct", 
                "sounds good", "looks good", "that's right", "exactly", 
                "yep", "yeah", "that is right", "that's correct"
            ]
            user_confirmed = any(word in user_content for word in satisfaction_words)
            
            # Find the last AI message that contains summary indicators
            # This is more robust than just finding the last AI message before user
            # because AI might have generated a duplicate summary
            summary_ai_msg = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    ai_content = msg.content.lower()
                    # Check if this AI message contains summary indicators
                    has_summary = (
                        "summary" in ai_content or 
                        "does this feel right" in ai_content or
                        "does this summary" in ai_content or
                        "here's a summary" in ai_content or
                        "here is a summary" in ai_content or
                        "summary of your" in ai_content or
                        "feel right to you" in ai_content or
                        "does this summary feel right" in ai_content or
                        "quick summary" in ai_content or
                        "investment plan" in ai_content and ("summary" in ai_content or "feel right" in ai_content)
                    )
                    if has_summary:
                        summary_ai_msg = msg
                        break
            
            # Also check for duplicate summary pattern (AI repeating the same summary)
            # If we detect this pattern, it means we're in a loop and should skip
            if not summary_ai_msg and len(messages) >= 4:
                # Check if last two AI messages are similar (duplicate summary)
                ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
                if len(ai_messages) >= 2:
                    last_ai = ai_messages[-1].content.lower()
                    second_last_ai = ai_messages[-2].content.lower()
                    # If last two AI messages are very similar and contain summary keywords
                    if ("summary" in last_ai or "feel right" in last_ai) and \
                       ("summary" in second_last_ai or "feel right" in second_last_ai):
                        # Check similarity (simple check: if they share key phrases)
                        key_phrases = ["investment plan", "funding amount", "valuation", "exit strategy"]
                        shared_phrases = sum(1 for phrase in key_phrases if phrase in last_ai and phrase in second_last_ai)
                        if shared_phrases >= 2:  # At least 2 key phrases match
                            logger.warning("Detected duplicate summary pattern - forcing skip to break loop")
                            summary_ai_msg = ai_messages[-1]  # Use last AI message
            
            # Check if we're in the last section
            current_section = state.get("current_section")
            is_last_section = current_section == SectionID.INVEST_PLAN if current_section else False
            
            # If we found a summary AI message, check if user confirmed it
            if summary_ai_msg:
                ai_content = summary_ai_msg.content.lower()
                ai_showed_summary = True
            else:
                ai_showed_summary = False
                ai_content = ""
            
            # Log for debugging
            logger.info(f"Checking skip conditions: is_last_section={is_last_section}, ai_showed_summary={ai_showed_summary}, user_confirmed={user_confirmed}")
            logger.info(f"User message: {user_content[:100]}")
            if summary_ai_msg:
                logger.info(f"Found summary AI message: {ai_content[:200]}")
            else:
                logger.warning("No summary AI message found in recent messages")
            
            # If user confirmed summary in last section, skip generating reply
            # This allows memory_updater to route to business plan generation
            if is_last_section and ai_showed_summary and user_confirmed:
                logger.info("User confirmed final summary - skipping reply generation to allow business plan generation")
                logger.info(f"Conditions: is_last_section={is_last_section}, ai_showed_summary={ai_showed_summary}, user_confirmed={user_confirmed}")
                # Don't generate a reply, just return state
                # The memory_updater will handle routing to business plan generation
                return state
    
    context_packet = state.get('context_packet')
    
    # Get LLM - no tools, no structured output for streaming
    llm = get_model()
    
    messages: list[BaseMessage] = []

    # Section-specific system prompt from context packet
    if state.get("context_packet"):
        messages.append(SystemMessage(content=state["context_packet"].system_prompt))

        # Add progress information
        section_names = {
            "mission": "Mission",
            "idea": "Idea",
            "team_traction": "Team & Traction",
            "invest_plan": "Investment Plan"
        }
        
        completed_sections = []
        for section_id, section_state in state.get("section_states", {}).items():
            if section_state.status == SectionStatus.DONE:
                section_name = section_names.get(section_id, section_id)
                completed_sections.append(section_name)
        
        current_section_name = section_names.get(state["current_section"].value, state["current_section"].value)
        
        progress_info = (
            f"\n\nSYSTEM STATUS:\n"
            f"- Total sections: 4\n"
            f"- Completed: {len(completed_sections)} sections"
        )
        if completed_sections:
            progress_info += f" ({', '.join(completed_sections)})"
        progress_info += f"\n- Currently working on: {current_section_name}\n"
        
        messages.append(SystemMessage(content=progress_info))
        
        # Add clarification for new sections without content
        current_section_id = state["current_section"].value
        section_state = state.get("section_states", {}).get(current_section_id)
        if not section_state or not section_state.content:
            new_section_instruction = (
                f"IMPORTANT: You are now in the {current_section_id} section. "
                "This is a NEW section with no content yet. "
                "Start by following the conversation flow defined in the section prompt. "
                "Do NOT reference or include content from previous sections."
            )
            messages.append(SystemMessage(content=new_section_instruction))

    # Recent conversation memory
    messages.extend(state.get("short_memory", []))

    # Last human message (if any and agent hasn't replied yet)
    if state.get("messages"):
        _last_msg = state["messages"][-1]
        if isinstance(_last_msg, HumanMessage):
            messages.append(_last_msg)

    # Generate reply
    response = await llm.ainvoke(messages)
    
    # Extract content
    reply_content = response.content if hasattr(response, 'content') else str(response)
    
    # Create AI message
    ai_message = AIMessage(content=reply_content)
    
    # Add to messages
    state["messages"].append(ai_message)
    
    # Update short_memory (keep last 10 messages)
    short_memory = state.get("short_memory", [])
    short_memory.append(ai_message)
    if len(short_memory) > 10:
        short_memory = short_memory[-10:]
    state["short_memory"] = short_memory
    
    # Set awaiting_user_input flag
    state["awaiting_user_input"] = True
    
    logger.info(f"Generated reply for section {state['current_section'].value}")
    
    return state

