"""Generate business plan node for Founder Buddy Agent."""

import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from core.llm import get_model

from ..enums import SectionStatus
from ..models import FounderBuddyState

logger = logging.getLogger(__name__)


async def generate_business_plan_node(state: FounderBuddyState | dict, config: RunnableConfig) -> FounderBuddyState | dict:
    """
    Generate a comprehensive business plan document from all collected data.
    
    This node is called when all sections are complete to create a final summary document.
    """
    logger.info("Generating business plan document")
    
    # Handle both dict and FounderBuddyState types
    if isinstance(state, dict):
        messages = state.get("messages", [])
        founder_data = state.get("founder_data", {})
    else:
        messages = state.get("messages", [])
        founder_data = state.get("founder_data", {})
    
    # Extract conversation history as text
    conversation_text = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation_text += f"User: {msg.content}\n\n"
        elif isinstance(msg, AIMessage):
            conversation_text += f"AI: {msg.content}\n\n"
    
    # Create business plan generation prompt
    system_prompt = """You are a professional business plan writer helping founders create a comprehensive business plan document.

Based on the complete conversation history, create a well-structured business plan document in English that includes:

# Business Plan

## 1. Executive Summary
- Business concept overview
- Core value proposition
- Target market

## 2. Mission & Vision
- Mission statement
- Vision statement
- Target audience

## 3. Product/Service Description
- Product description
- Core value proposition
- Key features
- Differentiation advantages

## 4. Team & Traction
- Team members and roles
- Key milestones
- Traction metrics

## 5. Investment Plan
- Funding amount
- Funding use
- Valuation
- Exit strategy

## 6. Next Steps
- Immediate action items
- Key milestones

Requirements:
- Use Markdown format with clear structure
- Content should be comprehensive but concise, approximately 2-3 pages
- Base all information on actual conversation content, do not use placeholders
- Use professional but accessible language
- Ensure all information comes from the conversation content"""

    messages_for_llm = [
        SystemMessage(content=system_prompt),
        SystemMessage(content=f"""
Complete conversation history:

{conversation_text}

Please generate a complete business plan based on the above conversation content. Ensure all information comes from the actual conversation content.
""")
    ]
    
    # Generate business plan
    llm = get_model()
    response = await llm.ainvoke(messages_for_llm)
    
    business_plan_content = response.content if hasattr(response, 'content') else str(response)
    
    # Add business plan to state
    state["business_plan"] = business_plan_content
    
    # Save to Supabase database
    try:
        from integrations.supabase import SupabaseClient
        supabase = SupabaseClient()
        
        # Get user_id and thread_id from state
        # These should be set by initialize_node, but we'll also check config as fallback
        user_id = state.get("user_id")
        thread_id = state.get("thread_id")
        
        # Fallback: If not in state, try to get from config (shouldn't be necessary if initialize_node works correctly)
        if not user_id or not thread_id:
            logger.warning(f"⚠️ user_id or thread_id missing from state! user_id={user_id}, thread_id={thread_id}")
            if config:
                # Handle both dict and RunnableConfig types
                if isinstance(config, dict):
                    configurable = config.get("configurable", {})
                else:
                    configurable = getattr(config, "configurable", {})
                
                if not user_id:
                    user_id = configurable.get("user_id")
                if not thread_id:
                    thread_id = configurable.get("thread_id")
                logger.info(f"Retrieved from config - user_id: {user_id}, thread_id: {thread_id}")
        
        logger.info(f"Attempting to save business plan - user_id: {user_id}, thread_id: {thread_id}")
        
        if user_id and thread_id:
            # Save business plan to database (Supabase client is synchronous)
            import asyncio
            loop = asyncio.get_event_loop()
            logger.info(f"Calling Supabase save_business_plan for user {user_id}, thread {thread_id}")
            save_result = await loop.run_in_executor(
                None,
                lambda: supabase.save_business_plan(
                    user_id=user_id,
                    thread_id=thread_id,
                    content=business_plan_content,
                    markdown_content=business_plan_content,  # Same content for now
                    agent_id="founder-buddy"
                )
            )
            
            logger.info(f"Supabase save_business_plan returned: {save_result}")
            
            if save_result.get("success"):
                logger.info(f"✅ Business plan saved to Supabase for user {user_id}, thread {thread_id}")
            else:
                logger.warning(f"❌ Failed to save business plan to Supabase: {save_result.get('error')}")
        else:
            logger.warning(f"⚠️ Cannot save business plan: user_id={user_id}, thread_id={thread_id} (one or both are None)")
    except ImportError as e:
        logger.warning(f"⚠️ Supabase not configured, skipping database save: {e}")
    except Exception as e:
        logger.error(f"❌ Failed to save business plan to Supabase: {e}", exc_info=True)
        # Don't fail the node if DB save fails
    
    # Get the last AI message to append business plan to it
    messages = state.get("messages", [])
    last_ai_message = None
    last_ai_index = -1
    for i in range(len(messages) - 1, -1, -1):
        if isinstance(messages[i], AIMessage):
            last_ai_message = messages[i]
            last_ai_index = i
            break
    
    # Create final message with business plan
    # Format: insert business plan into the completion message
    if last_ai_message and ("covered all the sections" in last_ai_message.content.lower() or 
                            "we've covered all" in last_ai_message.content.lower()):
        # Check if message already has "If there's anything else" part
        original_content = last_ai_message.content
        if "if there's anything else" in original_content.lower():
            # Split at "If there's anything else" and insert business plan before it
            parts = original_content.split("If there's anything else", 1)
            if len(parts) == 2:
                completion_part = parts[0].strip()
                ending_part = "If there's anything else" + parts[1]
            else:
                completion_part = original_content
                ending_part = "\n\nIf there's anything else you want to revisit or refine, let me know."
        else:
            completion_part = original_content
            ending_part = "\n\nIf there's anything else you want to revisit or refine, let me know."
        
        # Create final message with business plan inserted
        final_message = f"""{completion_part}

Here's the business plan:

---

{business_plan_content}

---

{ending_part}"""
        
        # Replace the last AI message instead of appending a new one
        state["messages"][last_ai_index] = AIMessage(content=final_message)
    else:
        # Fallback: create new message if we can't find the completion message
        final_message = f"""Great. With the investment plan clarified, we've covered all the sections. Here's the business plan:

---

{business_plan_content}

---

If there's anything else you want to revisit or refine, let me know."""
        
        # Add final message
        state["messages"].append(AIMessage(content=final_message))
    
    # Mark as finished and clear the flag
    state["finished"] = True
    state["should_generate_business_plan"] = False
    
    logger.info("Business plan generated successfully")
    logger.info(f"Final message added to state with content length: {len(final_message)}")
    
    return state

