"""Signature Pitch Agent implementation using LangGraph StateGraph."""

import logging
import re
from typing import Literal

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from core.llm import get_model, LLMConfig

from .models import (
    ChatAgentOutput,
    ContextPacket,
    ActiveChangeData,
    SpecificWhoData,
    OutcomePrizeData,
    CoreCredibilityData,
    StorySparkData,
    SignatureLineData,
    RouterDirective,
    SectionContent,
    SignaturePitchSectionID,
    SectionState,
    SectionStatus,
    TiptapDocument,
    SignaturePitchData,
    SignaturePitchState,
)
from .prompts import (
    get_next_unfinished_section,
    SECTION_TEMPLATES,
)
from .tools import (
    create_tiptap_content,
    export_signature_pitch_framework,
    extract_plain_text,
    get_all_sections_status,
    get_context,
    save_section,
    validate_field,
)

logger = logging.getLogger(__name__)


# Tools used by specific nodes
router_tools = [
    get_context,
]

memory_updater_tools = [
    save_section,
    get_all_sections_status,
    create_tiptap_content,
    extract_plain_text,
    validate_field,
]

implementation_tools = [
    export_signature_pitch_framework,
]

# Tools will be called directly within nodes (following social pitch pattern)


async def initialize_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Initialize node that ensures all required state fields are present.
    This is the first node in the graph to handle LangGraph Studio's incomplete state.
    """
    logger.info("Initialize node - Setting up default values")

    # CRITICAL FIX: Get correct IDs from config instead of using temp IDs
    # service.py now passes the correct user_id and thread_id through config
    configurable = config.get("configurable", {})
    
    if "user_id" not in state or not state["user_id"]:
        # Try to get user_id from config first
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
            logger.info(f"Initialize node - Got user_id from config: {state['user_id']}")
        else:
            logger.error("CRITICAL: Initialize node running without a user_id in both state and config!")
            raise ValueError(
                "Critical system error: No valid user_id found. "
                "This indicates a serious ID chain break that will cause data loss. "
                "Check service.py ID passing logic."
            )
    
    if "thread_id" not in state or not state["thread_id"]:
        # Try to get thread_id from config
        if "thread_id" in configurable and configurable["thread_id"]:
            state["thread_id"] = configurable["thread_id"]
            logger.info(f"Initialize node - Got thread_id from config: {state['thread_id']}")
        else:
            logger.error("CRITICAL: Initialize node running without a thread_id in state or config!")
            raise ValueError(
                "Critical system error: No valid thread_id found. "
                "This indicates a serious ID chain break that will cause data loss. "
                "Check service.py ID passing logic."
            )

    # Ensure all other required fields have default values
    if "current_section" not in state:
        state["current_section"] = SignaturePitchSectionID.ACTIVE_CHANGE
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.NEXT
    if "finished" not in state:
        state["finished"] = False
    if "section_states" not in state:
        state["section_states"] = {}
    if "canvas_data" not in state:
        state["canvas_data"] = SignaturePitchData()
    if "short_memory" not in state:
        state["short_memory"] = []
    if "error_count" not in state:
        state["error_count"] = 0
    if "last_error" not in state:
        state["last_error"] = None
    if "is_awaiting_rating" not in state:
        state["is_awaiting_rating"] = False
    if "messages" not in state:
        state["messages"] = []
    
    logger.info(f"Initialize complete - User: {state['user_id']}, Thread: {state['thread_id']}")
    return state


async def router_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Router node that handles navigation and context loading.
    
    Responsibilities:
    - Process router directives (stay, next, modify:section_id)
    - Update current_section
    - Call get_context when changing sections
    - Check for completion and set finished flag
    """
    # Check if there's a new user message - if so, reset awaiting_user_input
    msgs = state.get("messages", [])
    if msgs and len(msgs) >= 2:
        last_msg = msgs[-1]
        second_last_msg = msgs[-2]
        # If last message is human and second last is AI, user has responded
        if isinstance(last_msg, HumanMessage) and isinstance(second_last_msg, AIMessage):
            state["awaiting_user_input"] = False

    logger.info(
        f"Router node - Current section: {state['current_section']}, Directive: {state['router_directive']}"
    )

    # Process router directive
    directive = state.get("router_directive", RouterDirective.STAY)
    
    
    if directive == RouterDirective.STAY:
        # Stay on current section, no context reload needed
        logger.info("Staying on current section")
        return state
    
    elif directive == RouterDirective.NEXT:
        # Find next unfinished section
        logger.info(f"DEBUG: Preparing to find next section. Current section states: {state.get('section_states', {})})")
        
        # DEBUG: Log current section and its state before transition
        current_section_id = state["current_section"].value
        logger.info(f"TRANSITION_DEBUG: Leaving section {current_section_id}")
        if current_section_id in state.get("section_states", {}):
            current_state = state["section_states"][current_section_id]
            logger.info(f"TRANSITION_DEBUG: Section {current_section_id} final state - status: {current_state.status}, has_content: {bool(current_state.content)}")
        
        next_section = get_next_unfinished_section(state.get("section_states", {}))
        logger.info(f"DEBUG: get_next_unfinished_section decided the next section is: {next_section}")
        
        if next_section:
            logger.info(f"Moving to next section: {next_section}")
            
            previous_section = state["current_section"]
            state["current_section"] = next_section

            # Only clear short_memory when transitioning to a different section
            if previous_section != next_section:
                state["short_memory"] = []
                logger.info(f"Cleared short_memory for new section {next_section.value}")
            else:
                logger.info(f"Preserved short_memory on same-section NEXT directive for {next_section.value}")

            # Get context for new section
            logger.debug(f"DATABASE_DEBUG: Router calling get_context for section {next_section.value}")
            context = await get_context.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": next_section.value,
                "canvas_data": state["canvas_data"].model_dump(),
            })
            logger.debug(f"DATABASE_DEBUG: get_context returned for section {next_section.value}")
            
            state["context_packet"] = ContextPacket(**context)
            
            # Reset directive to STAY to prevent repeated transitions
            state["router_directive"] = RouterDirective.STAY
        else:
            # All sections complete
            logger.info("All sections complete, setting finished flag")
            state["finished"] = True
    
    elif directive.startswith("modify:"):
        # Jump to specific section
        section_id = directive.split(":", 1)[1].lower()  # handle case-insensitive IDs
        try:
            new_section = SignaturePitchSectionID(section_id)
            logger.info(f"Jumping to section: {new_section}")
            prev_section = state.get("current_section")
            state["current_section"] = new_section
            
            # Only clear short_memory when switching to a different section
            if prev_section != new_section:
                state["short_memory"] = []
                logger.info(f"Cleared short_memory for jumped section {new_section.value}")
            else:
                logger.info(f"Preserved short_memory for same-section refresh {new_section.value}")
            
            # Get context for new section
            logger.debug(f"DATABASE_DEBUG: Router calling get_context for modify section {new_section.value}")
            context = await get_context.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": new_section.value,
                "canvas_data": state["canvas_data"].model_dump(),
            })
            logger.debug(f"DATABASE_DEBUG: get_context returned for modify section {new_section.value}")
            
            state["context_packet"] = ContextPacket(**context)
            
            # Reset directive to STAY to prevent repeated transitions
            state["router_directive"] = RouterDirective.STAY
        except ValueError:
            logger.error(f"Invalid section ID: {section_id}")
            state["last_error"] = f"Invalid section ID: {section_id}"
            state["error_count"] += 1
    
    return state


async def chat_agent_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Chat agent node that handles section-specific conversations.
    
    Responsibilities:
    - Generate responses based on context_packet system prompt
    - Validate user input
    - Generate section content (Tiptap JSON)
    - Set score and router_directive
    - Output structured ChatAgentOutput
    """
    logger.info(f"Chat agent node - Section: {state['current_section']}")
    
    # DEBUG: Log recent message history
    # Create a new context packet for this turn
    context_packet = state.get('context_packet')
    logger.info(
        f"DEBUG_CHAT_AGENT: Context Packet received: {context_packet}"
    )

    # Get LLM - no tools for chat agent per design doc
    # Use centralized configuration
    llm = get_model()
    
    messages: list[BaseMessage] = []
    last_human_msg: HumanMessage | None = None

    # Check if we should add summary instruction
    # Add summary instruction when:
    # 1. We're not already awaiting user input
    # 2. User hasn't provided a rating
    # 3. We have collected enough information in the conversation (check short_memory)
    awaiting = state.get("awaiting_user_input", False)
    current_section = state["current_section"]
    section_state = state.get("section_states", {}).get(current_section.value)
    section_has_content = bool(section_state and section_state.content)
    
    # DEBUG: Log detailed section state info
    
    # IMPORTANT: Do NOT automatically trigger summary instructions
    # According to the design document, the Agent should decide when to show summary
    # based on whether it has collected all required information for the section.
    # The prompts in prompts.py already contain the logic for when to show summaries.
    # Forcing summary instructions here causes premature summaries.
    
    # Only add summary reminder if section already has saved content that needs rating
    if section_has_content and not awaiting:
        # This is for sections that were previously saved but need rating
        summary_reminder = (
            "The user has previously worked on this section. "
            "Review the saved content and ask for their satisfaction rating if not already provided."
        )
        messages.append(SystemMessage(content=summary_reminder))
        logger.info(f"SUMMARY_REMINDER: Added reminder to check existing content for section {current_section.value}")

    # 2) Section-specific system prompt from context packet
    if state.get("context_packet"):
        # NEW: Prioritize displaying existing section content if available
        current_section_id = state["current_section"].value
        section_state = state.get("section_states", {}).get(current_section_id)

        if section_state and section_state.content:
            logger.info(f"MEMORY_DEBUG: Found existing content for {current_section_id}. Prioritizing it.")
            try:
                # Use the plain_text version if available, otherwise extract it.
                # Note: content in section_states is now a SectionContent object.
                content_dict = section_state.content.content.model_dump()
                plain_text_summary = await extract_plain_text.ainvoke({"tiptap_json": content_dict})

                review_prompt = (
                    "CRITICAL CONTEXT: The user is reviewing a section they have already completed. "
                    "Their previous answers have been saved. Your primary task is to present this saved information back to them if they ask for it. "
                    "DO NOT ask the interview questions again. "
                    "Here is the exact summary of their previously provided answers. You MUST use this information:\n\n"
                    f"--- PREVIOUSLY SAVED SUMMARY ---\n{plain_text_summary}\n--- END SUMMARY ---"
                )
                messages.append(SystemMessage(content=review_prompt))
            except Exception as e:
                logger.error(f"MEMORY_DEBUG: Failed to extract plain text from existing state for {current_section_id}: {e}")
                # Fallback to the original prompt if extraction fails
                messages.append(SystemMessage(content=state["context_packet"].system_prompt))
        else:
            # Original behavior: use the default system prompt for the section
            messages.append(SystemMessage(content=state["context_packet"].system_prompt))

        # Add progress information based on section_states
        section_names = {
            "active_change": "Active Change",
            "specific_who": "Specific Who", 
            "outcome_prize": "Outcome/Prize",
            "core_credibility": "Core Credibility",
            "story_spark": "Story Spark",
            "signature_line": "Signature Line",
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
        
        # Add clarification for new sections without content
        current_section_id = state["current_section"].value
        section_state = state.get("section_states", {}).get(current_section_id)
        if not section_state or not section_state.content:
            new_section_instruction = (
                f"IMPORTANT: You are now in the {current_section_id} section. "
                "This is a NEW section with no content yet. "
                "Start by following the conversation flow defined in the section prompt. "
                "Do NOT generate section_update until you have collected actual data for THIS section. "
                "Do NOT reference or include content from previous sections."
            )
            messages.append(SystemMessage(content=new_section_instruction))

    # 3) Recent conversation memory
    # Keep all messages from short_memory.
    messages.extend(state.get("short_memory", []))

    # 4) Last human message (if any and agent hasn't replied yet)
    if state.get("messages"):
        _last_msg = state["messages"][-1]
        if isinstance(_last_msg, HumanMessage):
            messages.append(_last_msg)
            last_human_msg = _last_msg

    # --- Pre-LLM Context Injection ---
    # To prevent the LLM from hallucinating the next section's name, we calculate it
    # programmatically and provide it as a direct instruction.
    try:
        from .prompts import SECTION_TEMPLATES, get_next_unfinished_section
        
        temp_states = state.get("section_states", {}).copy()
        current_section_id = state["current_section"].value
        
        if current_section_id not in temp_states:
            temp_states[current_section_id] = SectionState(
                section_id=SignaturePitchSectionID(current_section_id),
                status=SectionStatus.DONE
            )
        else:
            # Assume the current section will be completed in this turn for prediction
            temp_states[current_section_id].status = SectionStatus.DONE

        next_section = get_next_unfinished_section(temp_states)
        
        if next_section:
            next_section_name = SECTION_TEMPLATES.get(next_section.value).name
            instructional_prompt = (
                f"SYSTEM INSTRUCTION: The next section is '{next_section_name}'. "
                "If the user confirms to proceed, you MUST use this exact name in your transition message."
            )
            messages.append(SystemMessage(content=instructional_prompt))
            logger.info(f"Injected next section name into context: '{next_section_name}'")
    except Exception as e:
        logger.warning(f"Could not determine next section for prompt injection: {e}")
    # --- End of Pre-LLM Context Injection ---

    try:
        # DEBUG: Log LLM input
        logger.info("=== LLM_INPUT_DEBUG ===")
        logger.info(f"Current section: {state['current_section']}")
        logger.info(f"Total messages count: {len(messages)}")
        logger.info("Last 2 messages:")
        for i, msg in enumerate(messages[-2:]):
            msg_type = type(msg).__name__
            content_preview = msg.content[:200] if hasattr(msg, 'content') else str(msg)[:200]
            logger.info(f"  [{i}] {msg_type}: {content_preview}...")
        
        # Use LangChain structured output with function calling for better reliability
        logger.info("🚀 Using LangChain structured output with function calling method")
        
        # Use function calling method which is more reliable than JSON parsing
        structured_llm = llm.with_structured_output(ChatAgentOutput, method="function_calling")
        
        # Add token limits to prevent infinite generation
        if hasattr(structured_llm, 'bind'):
            structured_llm = structured_llm.bind(
                max_tokens=LLMConfig.DEFAULT_MAX_TOKENS,
                top_p=LLMConfig.DEFAULT_TOP_P
            )
        
        logger.info("=== CALLING LLM WITH FUNCTION CALLING METHOD ===")
        llm_output = await structured_llm.ainvoke(messages)

        # DEBUG: Log the COMPLETE LLM output
        logger.info("=== LLM_OUTPUT_DEBUG ===")
        logger.info(f"Full reply: {llm_output.reply}")
        logger.info(f"Router directive: {llm_output.router_directive}")
        logger.info(f"Is requesting rating: {llm_output.is_requesting_rating}")
        logger.info(f"Score: {llm_output.score}")
        logger.info(f"Section update provided: {bool(llm_output.section_update)}")
        if llm_output.section_update:
            logger.info(f"Section update content keys: {list(llm_output.section_update.keys())}")
        else:
            logger.warning("❌ LLM did NOT provide section_update!")
        
        if llm_output.section_update:
            logger.warning(f"AGENT_OUTPUT_DEBUG: Section update generated for section {state['current_section'].value}")
            # Additional validation checks can be added here if needed

        # DEBUG: Check state consistency
        logger.info(f"AGENT_OUTPUT_DEBUG: Current section_states: {list(state.get('section_states', {}).keys())}")

        # Create the final agent_output for the state, starting with LLM output
        agent_output = llm_output
        
        # Rely entirely on the LLM for score.
        # Add a safety rail: if the LLM provides a low score, force a 'stay' directive
        # to ensure the user can revise the section, overriding any other directive.
        if agent_output.score is not None and agent_output.score < 3:
            logger.info(f"Low score ({agent_output.score}) detected from LLM. Forcing 'stay' directive.")
            agent_output.router_directive = "stay"

        # === SECTION_UPDATE ANALYSIS ===
        if agent_output.is_requesting_rating and not agent_output.section_update:
            logger.warning("=== SECTION_UPDATE_ANALYSIS ===")
            logger.warning("LLM is requesting rating but didn't provide section_update")
            
            # Analyze the reply to understand why
            reply_lower = agent_output.reply.lower()
            has_summary_keywords = any(keyword in reply_lower for keyword in [
                "summary", "gathered", "capture", "here's what", "information", 
                "active change:", "specific who:", "outcome:", "credibility:", "story:", "signature line:"
            ])
            
            logger.warning(f"Reply contains summary keywords: {has_summary_keywords}")
            logger.warning(f"Reply length: {len(agent_output.reply)}")
            logger.warning(f"Current section: {state['current_section']}")
            
            if has_summary_keywords:
                logger.error("🚨 LLM generated summary but FAILED to provide section_update!")
                logger.error("This indicates a prompt understanding issue or model limitation")
            
            logger.warning("Full LLM reply analysis:")
            logger.warning(f"Reply content: {agent_output.reply}")
            
        # Set the is_awaiting_rating flag based on the structured output from the LLM
        if agent_output.is_requesting_rating:
            # CRITICAL VALIDATION: If requesting rating, must have section_update
            if not agent_output.section_update:
                logger.error("CRITICAL ERROR: Model requested rating but provided no section_update!")
                logger.error("This violates the core system prompt rule and will cause data loss.")
                logger.error(f"Original agent_output: {agent_output}")
                
                # Force correction to prevent infinite loops
                agent_output = ChatAgentOutput(
                    reply=(
                        "I notice I haven't properly collected all your information yet. "
                        "Let me continue with the next question. "
                        "What specific transformation do you create for your clients?"
                    ),
                    router_directive="stay",
                    is_requesting_rating=False,
                    score=None,
                    section_update=None
                )
                logger.info("FORCED CORRECTION: Created new corrected agent output to continue collecting information.")
            
            state["is_awaiting_rating"] = agent_output.is_requesting_rating
            logger.info(f"State updated: is_awaiting_rating set to {agent_output.is_requesting_rating}")
        else:
            state["is_awaiting_rating"] = False


        logger.info(f"DEBUG_CHAT_AGENT: Agent output generated: {agent_output}")

        # Save section_update to a temporary key to be processed by the memory updater
        state["temp_agent_output"] = agent_output # Store the full agent_output for memory_updater

        # Determine router directive based on score, per design doc
        if agent_output.score is not None:
            if agent_output.score >= 3:
                calculated_directive = RouterDirective.NEXT
            else:
                calculated_directive = RouterDirective.STAY
                
            state["router_directive"] = calculated_directive
            
        else:
            # Fallback to value supplied by model (may be stay/next/modify)
            state["router_directive"] = agent_output.router_directive

        state["agent_output"] = agent_output

        # --- MVP Fallback: ensure reply contains clear question -----------------------
        need_question = (
            state["router_directive"] == RouterDirective.STAY
            and agent_output.score is None
        )

        if need_question:
            # If reply has neither question mark nor clear instruction words, append prompt
            has_question = re.search(r"[?？]", agent_output.reply, re.IGNORECASE)
            has_instruction = any(word in agent_output.reply.lower() for word in [
                "please", "provide", "describe", "tell", "share", "what", "how", "when", "where", "why"
            ])
            
            if not has_question and not has_instruction:
                # Only add fallback text when there's really no clear instruction
                agent_output.reply += (
                    "\n\nPlease provide your response to continue."
                )

        # ---------------------------------------------------------------

        # If we expect user input next, mark flag (MVP logic uses need_question)
        state["awaiting_user_input"] = need_question

        # Add AI reply to conversation history
        state["messages"].append(AIMessage(content=agent_output.reply))

        # Update short-term memory by appending new messages
        base_mem = state.get("short_memory", [])
        if last_human_msg is not None:
            base_mem.append(last_human_msg)
        base_mem.append(AIMessage(content=agent_output.reply))
        state["short_memory"] = base_mem

        # [DIAGNOSTIC] Log the output from the agent
        logger.info(f"DEBUG_CHAT_AGENT: Agent output generated: {state.get('agent_output')}")
        
        # [SAVE_SECTION_DEBUG] Track when Chat Agent generates section_update
        if state.get('agent_output') and state['agent_output'].section_update:
            logger.info(f"SAVE_SECTION_DEBUG: ✅ Chat Agent DID generate section_update for section {state['current_section']}")
            logger.debug(f"SAVE_SECTION_DEBUG: Section update content type: {type(state['agent_output'].section_update)}")
        else:
            logger.info(f"SAVE_SECTION_DEBUG: ❌ Chat Agent did NOT generate section_update for section {state['current_section']}")
            if state.get('agent_output'):
                logger.debug(f"SAVE_SECTION_DEBUG: Agent output exists but section_update is: {state['agent_output'].section_update}")
            else:
                logger.debug("SAVE_SECTION_DEBUG: No agent output exists at all")

    except Exception as e:
        logger.error(f"Failed to get structured output from LLM: {e}")
        default_output = ChatAgentOutput(
            reply="Sorry, I encountered a formatting error. Could you rephrase?",
            router_directive="stay",
            score=None,
            section_update=None,
        )
        state["agent_output"] = default_output
        state["router_directive"] = "stay"
        state["messages"].append(AIMessage(content=default_output.reply))
        state["awaiting_user_input"] = True
        state.setdefault("short_memory", []).append(AIMessage(content=default_output.reply))
    return state


async def memory_updater_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Memory updater node that persists section states and updates canvas data.
    Enhanced with sophisticated two-branch logic from Value Canvas.
    """
    logger.info("=== DATABASE_DEBUG: memory_updater_node() ENTRY ===")
    logger.info("DATABASE_DEBUG: Memory updater node processing agent output")
    
    agent_out = state.get("agent_output")
    logger.debug(f"DATABASE_DEBUG: Agent output exists: {bool(agent_out)}")
    if agent_out:
        logger.debug(f"DATABASE_DEBUG: Agent output - section_update: {bool(agent_out.section_update)}, score: {agent_out.score}, router_directive: {agent_out.router_directive}")

    # [DIAGNOSTIC] Log state before update
    logger.info(f"DATABASE_DEBUG: section_states BEFORE update: {state.get('section_states', {})}")
    logger.debug(f"DATABASE_DEBUG: Current section: {state.get('current_section')}")
    context_packet = state.get('context_packet')
    logger.debug(f"DATABASE_DEBUG: Context packet section: {context_packet.section_id if context_packet else None}")

    # Decide status based on score and directive
    def _status_from_output(score, directive):
        """Return status *string* to align with get_next_unfinished_section() logic."""
        if directive == RouterDirective.NEXT:
            return SectionStatus.DONE.value  # "done"
        if score is not None and score >= 3:
            return SectionStatus.DONE.value
        return SectionStatus.IN_PROGRESS.value

    # [SAVE_SECTION_DEBUG] Track decision path in memory_updater_node
    logger.info("SAVE_SECTION_DEBUG: memory_updater_node decision analysis:")
    logger.info(f"SAVE_SECTION_DEBUG: - agent_out exists: {bool(agent_out)}")
    if agent_out:
        logger.info(f"SAVE_SECTION_DEBUG: - agent_out.section_update exists: {bool(agent_out.section_update)}")
        logger.info(f"SAVE_SECTION_DEBUG: - agent_out.score: {agent_out.score}")
        logger.info(f"SAVE_SECTION_DEBUG: - agent_out.router_directive: {agent_out.router_directive}")
    else:
        logger.info("SAVE_SECTION_DEBUG: - No agent_out, will not call save_section")
    
    if agent_out and agent_out.section_update:
        # BRANCH 1: Process section_update (when LLM provides structured content)
        section_id = state["current_section"].value
        logger.info(f"SAVE_SECTION_DEBUG: ✅ ENTERING BRANCH 1: Processing section_update for section {section_id}")
        logger.info(f"DATABASE_DEBUG: Processing section_update for section {section_id}")
        logger.debug(f"DATABASE_DEBUG: Section update content type: {type(agent_out.section_update)}")
        
        # DEBUG: Log what content is being saved to which section
        logger.warning(f"CONTENT_DEBUG: About to save content to section {section_id}")
        if isinstance(agent_out.section_update, dict) and 'content' in agent_out.section_update:
            content_dict = agent_out.section_update['content']
            if isinstance(content_dict, dict) and 'content' in content_dict:
                # Try to extract first paragraph text for debugging
                try:
                    first_para = content_dict['content'][0]
                    if isinstance(first_para, dict) and 'content' in first_para:
                        first_text = first_para['content'][0].get('text', 'No text')
                        logger.warning(f"CONTENT_DEBUG: First paragraph starts with: {first_text[:100]}...")
                except Exception:
                    logger.warning("CONTENT_DEBUG: Could not extract content preview")
        
        # Save to database using save_section tool (make non-blocking for DB issues)
        logger.info("SAVE_SECTION_DEBUG: ✅ CALLING save_section with structured content")
        logger.debug("DATABASE_DEBUG: Calling save_section tool with structured content")
        
        # [CRITICAL DEBUG] Log the exact parameters being passed to save_section
        computed_status = _status_from_output(agent_out.score, agent_out.router_directive)
        logger.info("SAVE_SECTION_DEBUG: About to call save_section with:")
        logger.info(f"SAVE_SECTION_DEBUG: - user_id: {state['user_id']}")
        logger.info(f"SAVE_SECTION_DEBUG: - thread_id: {state['thread_id']}")
        logger.info(f"SAVE_SECTION_DEBUG: - section_id: {section_id}")
        logger.info(f"SAVE_SECTION_DEBUG: - score: {agent_out.score} (type: {type(agent_out.score)})")
        logger.info(f"SAVE_SECTION_DEBUG: - status: {computed_status} (type: {type(computed_status)})")
        logger.info(f"SAVE_SECTION_DEBUG: - router_directive was: {agent_out.router_directive} (type: {type(agent_out.router_directive)})")
        
        try:
            save_result = await save_section.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": section_id,
                "content": agent_out.section_update['content'] if isinstance(agent_out.section_update, dict) else agent_out.section_update,
                "score": agent_out.score,
                "status": computed_status,
            })
            logger.debug(f"DATABASE_DEBUG: save_section returned: {bool(save_result)}")
        except Exception as e:
            logger.warning(f"DATABASE_DEBUG: save_section failed (expected if DB not configured): {e}")
            # Continue with local state management even if database save fails
        
        # Update local state (this is critical for proper functioning)
        logger.debug("DATABASE_DEBUG: Updating local section_states with new content")
        # Parse the section_update content properly
        if isinstance(agent_out.section_update, dict) and 'content' in agent_out.section_update:
            tiptap_doc = TiptapDocument.model_validate(agent_out.section_update['content'])
        else:
            logger.error(f"SAVE_SECTION_DEBUG: Invalid section_update structure: {type(agent_out.section_update)}")
            tiptap_doc = TiptapDocument(type="doc", content=[])
        
        state["section_states"][section_id] = SectionState(
            section_id=SignaturePitchSectionID(section_id),
            content=SectionContent(
                content=tiptap_doc,
                plain_text=None  # Will be filled later if needed
            ),
            score=agent_out.score,
            status=_status_from_output(agent_out.score, agent_out.router_directive),
        )
        logger.info(f"SAVE_SECTION_DEBUG: ✅ BRANCH 1 COMPLETED: Section {section_id} saved with structured content")

        # Extract structured data and update canvas_data using LLM
        try:
            await extract_and_update_canvas_data(state, section_id, agent_out.section_update)
        except Exception as e:
            logger.warning(f"DATABASE_DEBUG: Failed to extract structured data (non-critical): {e}")
        
        logger.info(f"DATABASE_DEBUG: ✅ Section {section_id} updated with structured content")
        
        # Reset consecutive stays counter since we made progress
        state["consecutive_stays"] = 0
        
    # Handle cases where agent provides score/status but no structured section_update  
    elif agent_out:
        # BRANCH 2: Process agent output without section_update (when LLM provides score but no content)
        logger.info("SAVE_SECTION_DEBUG: ✅ ENTERING BRANCH 2: Processing agent output without section_update")
        logger.info("DATABASE_DEBUG: Processing agent output without section_update (likely score/status only)")
        
        if state.get("context_packet"):
            score_section_id = state["context_packet"].section_id.value
            logger.debug(f"DATABASE_DEBUG: Processing score/status update for section {score_section_id}")

            # Only proceed if there's a score to save.
            if agent_out.score is None:
                logger.info(f"DATABASE_DEBUG: No score or section_update for {score_section_id}, skipping save.")
                return state

            # We have a score, so we MUST save. We need to find the content.
            content_to_save = None

            # 1. Try to find content in the current state for the section
            if score_section_id in state.get("section_states", {}) and state["section_states"][score_section_id].content:
                logger.info(f"SAVE_SECTION_DEBUG: Found content for section {score_section_id} in state.")
                # The content in state should now be the correct Tiptap document
                content_to_save = state["section_states"][score_section_id].content.content.model_dump()
            
            # 2. If not in state, recover from previous message history with improved logic
            if not content_to_save:
                logger.warning(f"SAVE_SECTION_DEBUG: Content for {score_section_id} not in state, recovering from history.")
                messages = state.get("messages", [])
                summary_text = None
                # Search backwards through the message history to find the last summary message.
                for msg in reversed(messages):
                    if isinstance(msg, AIMessage):
                        # A summary message typically contains these keywords.
                        content_lower = msg.content.lower()
                        if "summary" in content_lower and ("satisfied" in content_lower or "rate 0-5" in content_lower):
                            summary_text = msg.content
                            logger.info("SAVE_SECTION_DEBUG: Found candidate summary message in history.")
                            break
                
                if summary_text:
                    logger.info("SAVE_SECTION_DEBUG: Recovered summary text, converting to Tiptap format.")
                    try:
                        content_to_save = await create_tiptap_content.ainvoke({"text": summary_text})
                    except Exception as e:
                        logger.error(f"SAVE_SECTION_DEBUG: Failed to convert summary to Tiptap: {e}")
                else:
                    logger.error(f"SAVE_SECTION_DEBUG: Could not recover summary from message history for {score_section_id}.")

            # 3. If we found content (either from state or recovery), proceed with saving.
            if content_to_save:
                computed_status = _status_from_output(agent_out.score, agent_out.router_directive)
                logger.info(f"SAVE_SECTION_DEBUG: ✅ Calling save_section for {score_section_id} with score and content.")
                
                try:
                    await save_section.ainvoke({
                        "user_id": state["user_id"],
                        "thread_id": state["thread_id"],
                        "section_id": score_section_id,
                        "content": content_to_save,
                        "score": agent_out.score,
                        "status": computed_status,
                    })
                except Exception as e:
                    logger.warning(f"DATABASE_DEBUG: save_section failed (expected if DB not configured): {e}")

                # Update local state consistently, whether it existed before or not.
                # Convert content_to_save to TiptapDocument
                if isinstance(content_to_save, dict):
                    tiptap_doc = TiptapDocument.model_validate(content_to_save)
                else:
                    tiptap_doc = content_to_save
                
                state.setdefault("section_states", {})[score_section_id] = SectionState(
                    section_id=SignaturePitchSectionID(score_section_id),
                    content=SectionContent(
                        content=tiptap_doc,
                        plain_text=None
                    ),
                    score=agent_out.score,
                    status=computed_status,
                )
                logger.info(f"DATABASE_DEBUG: ✅ Updated/created section state for {score_section_id} with score {agent_out.score}")
            else:
                # 4. If content recovery failed, we must not call save_section with empty content.
                logger.error(f"DATABASE_DEBUG: ❌ CRITICAL: Aborting save for section {score_section_id} due to missing content.")

        else:
            logger.warning("DATABASE_DEBUG: ⚠️ Cannot update section state as context_packet is missing")

    else:
        # No agent output at all - safety mechanism for stuck states
        logger.info("SAVE_SECTION_DEBUG: ❌ No agent_out - applying safety mechanism")
        
        # Safety mechanism: if we're stuck in stay mode without progress, force next
        if state.get("router_directive") == "stay":
            consecutive_stays = state.get("consecutive_stays", 0) + 1
            state["consecutive_stays"] = consecutive_stays
            
            if consecutive_stays >= 3:  # After 3 stays without progress, force next
                logger.warning("Memory updater node - Forcing next due to no progress after multiple stays")
                state["router_directive"] = "next" 
                state["consecutive_stays"] = 0

    # [SAVE_SECTION_DEBUG] Final decision summary
    if not agent_out:
        logger.info("SAVE_SECTION_DEBUG: ❌ FINAL RESULT: No agent_out - save_section was NEVER called")
    elif agent_out.section_update:
        logger.info("SAVE_SECTION_DEBUG: ✅ FINAL RESULT: Had section_update - save_section was called in BRANCH 1")
    elif agent_out:
        logger.info("SAVE_SECTION_DEBUG: ✅ FINAL RESULT: Had agent_out but no section_update - save_section was called in BRANCH 2 (if conditions met)")
    else:
        logger.info("SAVE_SECTION_DEBUG: ❌ FINAL RESULT: Unknown state - save_section may not have been called")
    
    # [DIAGNOSTIC] Log state after update
    logger.info(f"DATABASE_DEBUG: section_states AFTER update: {state.get('section_states', {})}")
    logger.info("=== DATABASE_DEBUG: memory_updater_node() EXIT ===")

    return state


async def extract_and_update_canvas_data(
    state: SignaturePitchState, 
    section_id: str, 
    section_update: dict
) -> None:
    """Extract structured data from section content and update canvas_data."""
    logger.info(f"Extracting structured data for section: {section_id}")
    
    # Get plain text from tiptap content
    plain_text = await extract_plain_text.ainvoke(section_update['content'])
    
    # Extract data based on section type
    llm = get_model()
    
    try:
        if section_id == SignaturePitchSectionID.ACTIVE_CHANGE.value:
            structured_llm = llm.with_structured_output(ActiveChangeData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract active change data from this content: {plain_text}")
            ])
            
            # Update canvas_data with extracted fields
            canvas_data = state["canvas_data"]
            if extracted_data.active_change:
                canvas_data.active_change = extracted_data.active_change
                
        elif section_id == SignaturePitchSectionID.SPECIFIC_WHO.value:
            structured_llm = llm.with_structured_output(SpecificWhoData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract specific who data from this content: {plain_text}")
            ])
            
            canvas_data = state["canvas_data"]
            if extracted_data.specific_who:
                canvas_data.specific_who = extracted_data.specific_who
            if extracted_data.target_audience:
                canvas_data.target_audience = extracted_data.target_audience
                
        elif section_id == SignaturePitchSectionID.OUTCOME_PRIZE.value:
            structured_llm = llm.with_structured_output(OutcomePrizeData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract outcome/prize data from this content: {plain_text}")
            ])
            
            canvas_data = state["canvas_data"]
            if extracted_data.outcome_prize:
                canvas_data.outcome_prize = extracted_data.outcome_prize
            if extracted_data.compelling_result:
                canvas_data.compelling_result = extracted_data.compelling_result
                
        elif section_id == SignaturePitchSectionID.CORE_CREDIBILITY.value:
            structured_llm = llm.with_structured_output(CoreCredibilityData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract core credibility data from this content: {plain_text}")
            ])
            
            canvas_data = state["canvas_data"]
            if extracted_data.core_credibility:
                canvas_data.core_credibility = extracted_data.core_credibility
            if extracted_data.proof_points:
                canvas_data.proof_points = extracted_data.proof_points
                
        elif section_id == SignaturePitchSectionID.STORY_SPARK.value:
            structured_llm = llm.with_structured_output(StorySparkData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract story spark data from this content: {plain_text}")
            ])
            
            canvas_data = state["canvas_data"]
            if extracted_data.story_spark:
                canvas_data.story_spark = extracted_data.story_spark
            if extracted_data.narrative_hook:
                canvas_data.narrative_hook = extracted_data.narrative_hook
                
        elif section_id == SignaturePitchSectionID.SIGNATURE_LINE.value:
            structured_llm = llm.with_structured_output(SignatureLineData)
            extracted_data = await structured_llm.ainvoke([
                SystemMessage(content=f"Extract signature line data from this content: {plain_text}")
            ])
            
            canvas_data = state["canvas_data"]
            if extracted_data.signature_line:
                canvas_data.signature_line = extracted_data.signature_line
            if extracted_data.ninety_second_pitch:
                canvas_data.ninety_second_pitch = extracted_data.ninety_second_pitch
        
        logger.info(f"Successfully extracted and updated canvas data for section: {section_id}")
        
    except Exception as e:
        logger.warning(f"Failed to extract structured data for section {section_id}: {e}")
        # Continue without structured extraction - the content is still saved


async def implementation_node(state: SignaturePitchState, config: RunnableConfig) -> SignaturePitchState:
    """
    Implementation node that generates final signature pitch framework exports.
    """
    logger.info("Implementation node - Generating signature pitch framework")
    
    try:
        # Generate signature pitch framework export
        framework_content = await export_signature_pitch_framework.ainvoke({
            "user_id": state["user_id"],
            "thread_id": state["thread_id"],
            "canvas_data": state["canvas_data"].model_dump(),
        })
        
        # Create implementation response
        response_content = f"Your complete Signature Pitch Framework has been generated:\\n\\n{framework_content}"
        
        state["messages"].append(AIMessage(content=response_content))
        state["finished"] = True
        
        logger.info("Implementation node - Successfully generated signature pitch framework")
        
    except Exception as e:
        logger.error(f"Implementation node - Error generating framework: {e}")
        fallback_response = "I apologize, but there was an error generating your signature pitch framework. Please try again."
        state["messages"].append(AIMessage(content=fallback_response))
        state["error_count"] = state.get("error_count", 0) + 1
        state["last_error"] = str(e)
    
    return state


def route_decision(state: SignaturePitchState) -> Literal["implementation", "chat_agent", "halt"]:
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
        from langchain_core.messages import (  # local import to avoid circular
            HumanMessage,
        )
        # If last message is from user, agent hasn't replied yet
        return isinstance(last_msg, HumanMessage)
    
    directive = state.get("router_directive")
    
    # 2. STAY directive - continue on current section
    if directive == RouterDirective.STAY or (isinstance(directive, str) and directive.lower() == "stay"):
        # If the user has replied since last AI message, forward to Chat Agent.
        if has_pending_user_input():
            return "chat_agent"

        # If AI is still waiting for user response, halt and wait for next run (prevent repeated questions).
        if state.get("awaiting_user_input", False):
            return "halt"

        # Otherwise, halt directly (typically when just initialized).
        return "halt"
    
    # 3. NEXT/MODIFY directive - section transition  
    elif directive == RouterDirective.NEXT or (isinstance(directive, str) and directive.startswith("modify:")):
        # For NEXT/MODIFY directives, we need to let the router handle the transition
        # and then ask the first question for the new section
        
        # If there's a pending user input, it means user has acknowledged the transition
        # Let router process the directive and then go to chat_agent for new section
        if has_pending_user_input():
            return "chat_agent"
        
        # If Chat Agent just set NEXT directive but user hasn't responded yet, halt and wait
        msgs = state.get("messages", [])
        if msgs and isinstance(msgs[-1], AIMessage):
            return "halt"
        
        # Default case - go to chat_agent to ask first question of current section
        return "chat_agent"
    
    # 4. Default case - halt to prevent infinite loops
    return "halt"


# Build the graph
def build_signature_pitch_graph():
    """Build the Signature Pitch agent graph."""
    graph = StateGraph(SignaturePitchState)
    
    # Add nodes
    graph.add_node("initialize", initialize_node)
    graph.add_node("router", router_node)
    graph.add_node("chat_agent", chat_agent_node)
    graph.add_node("memory_updater", memory_updater_node)
    graph.add_node("implementation", implementation_node)
    
    # Add edges
    graph.add_edge(START, "initialize")
    graph.add_edge("initialize", "router")
    
    # Router can go to chat agent or implementation
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "chat_agent": "chat_agent",
            "implementation": "implementation",
            "halt": END,
        }
    )
    
    # Chat agent has no tools, goes directly to memory_updater
    graph.add_edge("chat_agent", "memory_updater")
    
    # Memory updater goes back to router
    graph.add_edge("memory_updater", "router")
    
    # Implementation ends the graph
    graph.add_edge("implementation", END)
    
    return graph.compile()


# Create the runnable graph
graph = build_signature_pitch_graph()


async def initialize_signature_pitch_state(user_id: int = None, thread_id: str = None) -> SignaturePitchState:
    """Initialize a new Signature Pitch state.
    
    Args:
        user_id: Integer user ID from frontend (will use default if not provided)
        thread_id: Thread UUID (will be generated if not provided)
    """
    import uuid
    
    # Use provided integer user_id or default to 1
    if not user_id:
        user_id = 1
        logger.info(f"Using default user_id: {user_id}")
    else:
        logger.info(f"Using provided user_id: {user_id}")

    # Ensure thread_id is a valid UUID string
    if not thread_id:
        thread_id = str(uuid.uuid4())
        logger.info(f"Generated new thread_id: {thread_id}")
    else:
        try:
            uuid.UUID(thread_id)
        except ValueError:
            thread_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, thread_id))
            logger.info(f"Converted non-UUID thread_id to UUID: {thread_id}")
    
    initial_state = SignaturePitchState(
        user_id=user_id,
        thread_id=thread_id,
        messages=[],
        current_section=SignaturePitchSectionID.ACTIVE_CHANGE,
        router_directive=RouterDirective.NEXT,  # Start by loading first section
    )
    
    # Get initial context
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": SignaturePitchSectionID.ACTIVE_CHANGE.value,
        "canvas_data": {},
    })
    
    initial_state["context_packet"] = ContextPacket(**context)
    
    # Add welcome message
    welcome_msg = AIMessage(
        content="Welcome! I'm here to help you create your Signature Pitch - "
        "a powerful 90-second magnetic pitch that captures attention, builds credibility, and creates desire. "
        "Let's start by defining your Active Change - the transformation you create in the world."
    )
    initial_state["messages"].append(welcome_msg)
    
    return initial_state




__all__ = ["graph", "initialize_signature_pitch_state"]