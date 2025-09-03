"""Chat agent node for Mission Pitch Agent."""

import logging

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model
from ..models import MissionPitchState, ChatAgentOutput, SectionStatus

logger = logging.getLogger(__name__)


async def chat_agent_node(state: MissionPitchState, config: RunnableConfig) -> MissionPitchState:
    """
    Chat agent node that handles section-specific conversations.
    This node has NO tools and only does conversation generation.
    """
    logger.info("Chat agent node - Starting conversation generation")
    
    # Get LLM with structured output
    llm = get_model()
    structured_llm = llm.with_structured_output(ChatAgentOutput, method="function_calling")
    
    # Build message context
    messages: list[BaseMessage] = []
    
    # Add system prompt from context packet
    if state.get("context_packet"):
        system_content = state["context_packet"].system_prompt
        messages.append(SystemMessage(content=system_content))
        logger.debug("Chat agent node - Added system prompt from context packet")

        # Add progress information based on section_states
        section_names = {
            "hidden_theme": "Hidden Theme",
            "personal_origin": "Personal Origin", 
            "business_origin": "Business Origin",
            "mission": "Mission",
            "three_year_vision": "3-Year Vision",
            "big_vision": "Big Vision",
            "implementation": "Implementation"
        }
        
        completed_sections = []
        for section_id, section_state in state.get("section_states", {}).items():
            if section_state.status == SectionStatus.DONE:
                section_name = section_names.get(section_id, section_id)
                completed_sections.append(section_name)
        
        current_section_name = section_names.get(state["current_section"].value, state["current_section"].value)
        
        progress_info = (
            f"\n\nSYSTEM STATUS:\n"
            f"- Total sections: 7\n"
            f"- Completed: {len(completed_sections)} sections"
        )
        if completed_sections:
            progress_info += f" ({', '.join(completed_sections)})"
        progress_info += f"\n- Currently working on: {current_section_name}\n"
        
        messages.append(SystemMessage(content=progress_info))
    
    # Add conversation history (short memory)
    if state.get("short_memory"):
        messages.extend(state["short_memory"])
        logger.debug(f"Chat agent node - Added {len(state['short_memory'])} messages from short memory")
    
    # Add the last human message from the main conversation
    if state.get("messages"):
        last_msg = state["messages"][-1]
        if isinstance(last_msg, HumanMessage):
            messages.append(last_msg)
            logger.debug("Chat agent node - Added last human message")
    
    # Get structured output from LLM
    try:
        logger.info("Chat agent node - Calling LLM for response generation")
        llm_output = await structured_llm.ainvoke(messages)
        logger.info("Chat agent node - Successfully got structured output from LLM")
        
        # Store the structured output for downstream processing
        state["agent_output"] = llm_output
        
        # Update router directive from LLM output
        state["router_directive"] = llm_output.router_directive
        
        # Add AI response to messages
        state["messages"].append(AIMessage(content=llm_output.reply))
        
        # Update short memory - keep last 10 messages
        all_messages = state.get("messages", [])
        state["short_memory"] = all_messages[-10:] if len(all_messages) > 10 else all_messages
        
        # Set waiting flags
        state["awaiting_user_input"] = True
        state["is_awaiting_rating"] = llm_output.is_requesting_rating
        
        logger.info(f"Chat agent node - Set router directive to: {llm_output.router_directive}")
        
    except Exception as e:
        logger.error(f"Chat agent node - Error during LLM call: {e}")
        state["error_count"] = state.get("error_count", 0) + 1
        state["last_error"] = str(e)
        
        # Create fallback response
        fallback_output = ChatAgentOutput(
            reply="I apologize, but I encountered an error. Please try again.",
            router_directive="stay",
        )
        state["agent_output"] = fallback_output
        state["messages"].append(AIMessage(content=fallback_output.reply))
    
    return state
