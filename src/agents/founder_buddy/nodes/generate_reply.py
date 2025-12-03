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
    # IMPORTANT: Reload latest business_plan from Supabase if Realtime sync is enabled
    # This ensures Agent sees the latest changes made by the user
    try:
        from core.settings import settings
        logger.info(f"🔄 Generate reply: Checking USE_SUPABASE_REALTIME={settings.USE_SUPABASE_REALTIME}")
        
        if settings.USE_SUPABASE_REALTIME:
            from integrations.supabase import SupabaseClient
            supabase = SupabaseClient()
            
            # Handle both dict and RunnableConfig types
            if isinstance(config, dict):
                configurable = config.get("configurable", {})
            else:
                configurable = getattr(config, "configurable", {}) if hasattr(config, "configurable") else {}
            
            # Get user_id and thread_id from config or state
            user_id = None
            thread_id = None
            
            if isinstance(configurable, dict):
                user_id = configurable.get("user_id")
                thread_id = configurable.get("thread_id")
            elif hasattr(configurable, "get"):
                user_id = configurable.get("user_id")
                thread_id = configurable.get("thread_id")
            
            # Fallback to state if not in config
            if not user_id:
                if isinstance(state, dict):
                    user_id = state.get("user_id")
                elif hasattr(state, "user_id"):
                    user_id = getattr(state, "user_id", None)
            
            if not thread_id:
                if isinstance(state, dict):
                    thread_id = state.get("thread_id")
                elif hasattr(state, "thread_id"):
                    thread_id = getattr(state, "thread_id", None)
            
            logger.info(f"🔄 Generate reply: user_id={user_id}, thread_id={thread_id}")
            
            if user_id and thread_id:
                # Load latest business plan from Supabase
                latest_plan = supabase.get_business_plan(user_id, thread_id)
                logger.info(f"🔄 Generate reply: latest_plan={latest_plan is not None}, has_content={latest_plan.get('content') is not None if latest_plan else False}")
                
                if latest_plan:
                    latest_content = latest_plan.get("content") or latest_plan.get("markdown_content")
                    
                    # Handle both dict and FounderBuddyState types
                    if isinstance(state, dict):
                        current_business_plan = state.get("business_plan")
                    else:
                        current_business_plan = getattr(state, "business_plan", None) if hasattr(state, "business_plan") else None
                    
                    logger.info(f"🔄 Generate reply: latest_content length={len(latest_content) if latest_content else 0}, current length={len(current_business_plan) if current_business_plan else 0}")
                    
                    if latest_content:
                        if latest_content != current_business_plan:
                            logger.info(f"🔄 Generate reply: ✅ Reloaded latest business_plan from Supabase (length: {len(latest_content)})")
                            if isinstance(state, dict):
                                state["business_plan"] = latest_content
                            else:
                                setattr(state, "business_plan", latest_content)
                        else:
                            logger.info(f"🔄 Generate reply: Business plan already in sync (length: {len(latest_content)})")
                    else:
                        logger.info(f"🔄 Generate reply: No content in latest_plan")
                else:
                    logger.info(f"🔄 Generate reply: No business plan found in database")
            else:
                logger.info(f"🔄 Generate reply: Missing user_id or thread_id (user_id={user_id}, thread_id={thread_id})")
        else:
            logger.info(f"🔄 Generate reply: USE_SUPABASE_REALTIME is False, skipping reload")
    except Exception as e:
        logger.warning(f"❌ Could not reload business_plan from Supabase: {e}", exc_info=True)
        # Continue without reloading - not critical
    
    # IMPORTANT: Reset finished flag if user sent a message after business plan generation
    if state.get("finished", False) and state.get("messages"):
        last_msg = state["messages"][-1]
        if isinstance(last_msg, HumanMessage):
            logger.info("User sent message after business plan generation - resetting finished flag")
            state["finished"] = False
    
    logger.info(f"Generate reply node - Section: {state['current_section']}, finished={state.get('finished', False)}")
    
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
    
    # If business plan has been generated, add context about it
    if state.get("business_plan"):
        # Extract key information from business plan for context
        business_plan_content = state.get("business_plan", "")
        
        # Extract Investment Plan section for context (most likely to be edited)
        invest_plan_section = ""
        if "## 5. Investment Plan" in business_plan_content or "## 5. Investment Plan\n" in business_plan_content:
            invest_start = business_plan_content.find("## 5. Investment Plan")
            invest_end = business_plan_content.find("## 6. Next Steps", invest_start)
            if invest_end == -1:
                invest_end = len(business_plan_content)
            invest_plan_section = business_plan_content[invest_start:invest_end].strip()
        
        business_plan_context = (
            "\n\nIMPORTANT CONTEXT: A business plan has already been generated for this conversation. "
            "The user may have edited it directly in the editor. "
            "Here is the current Investment Plan section from the business plan:\n\n"
            f"{invest_plan_section}\n\n"
            "If the user mentions changes they made (e.g., 'I changed the valuation'), "
            "acknowledge that you can see the updated information and respond accordingly. "
            "Be helpful and responsive to their requests about the business plan."
        )
        messages.append(SystemMessage(content=business_plan_context))

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

