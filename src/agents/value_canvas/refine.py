"""Section refinement logic for Value Canvas Agent.

This module handles AI-powered refinement of section content based on user instructions.
"""

import logging
from typing import Any

from langchain_core.runnables import RunnableConfig

from core.llm import get_model
from integrations.dentapp.dentapp_client import get_dentapp_client
from integrations.dentapp.dentapp_utils import (
    AGENT_ID,
    get_section_id_int,
    plain_text_to_tiptap,
    tiptap_to_plain_text,
)

from .tools import get_context

logger = logging.getLogger(__name__)


async def refine_section_content(
    user_id: int,
    thread_id: str,
    section_id: str,
    refinement_prompt: str,
    agent_graph: Any  # AgentGraph type
) -> dict[str, Any]:
    """
    Refine a section's content using AI based on user's instruction.

    This function:
    1. Fetches current LangGraph state to get canvas_data
    2. Gets rendered section prompt with all dependencies via get_context()
    3. Fetches current section content from DentApp API
    4. Constructs refinement prompt with clear structure
    5. Calls OpenAI LLM to generate refined content
    6. Returns refined content in both plain text and Tiptap format

    Args:
        user_id: User identifier
        thread_id: Thread/conversation identifier
        section_id: Section identifier
        refinement_prompt: User's instruction for how to refine the content
        agent_graph: LangGraph agent instance

    Returns:
        Refinement result dictionary with refined content

    Raises:
        ValueError: If section_id is invalid
        Exception: If DentApp API call fails or LLM call fails
    """
    logger.info(f"=== REFINE_SECTION_START: section_id={section_id}, user={user_id}, thread={thread_id} ===")

    # Step 1: Get current LangGraph state to access canvas_data
    logger.info("REFINE: Step 1/5 - Getting current LangGraph state")
    config = RunnableConfig(
        configurable={
            "thread_id": thread_id,
            "user_id": user_id
        }
    )

    current_state = await agent_graph.aget_state(config)
    canvas_data = current_state.values.get("canvas_data", {})

    # Convert to dict if it's a Pydantic model
    if hasattr(canvas_data, 'model_dump'):
        canvas_data_dict = canvas_data.model_dump()
    else:
        canvas_data_dict = dict(canvas_data) if canvas_data else {}

    logger.debug(f"REFINE: Retrieved canvas_data with {len(canvas_data_dict)} fields")

    # Step 2: Get rendered section prompt with dependencies
    logger.info("REFINE: Step 2/5 - Getting rendered section prompt")
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": section_id,
        "canvas_data": canvas_data_dict,
    })

    rendered_section_prompt = context.get("system_prompt", "")
    logger.debug(f"REFINE: Retrieved system prompt (length: {len(rendered_section_prompt)})")

    # Step 3: Fetch current section content from DentApp API
    logger.info("REFINE: Step 3/5 - Fetching current content from DentApp API")
    dentapp_client = get_dentapp_client()

    if not dentapp_client:
        logger.error("REFINE_ERROR: DentApp API client not available")
        raise Exception("DentApp API is not configured")

    section_id_int = get_section_id_int(section_id)
    if section_id_int is None:
        logger.error(f"REFINE_ERROR: Cannot map section_id {section_id} to integer")
        raise ValueError(f"Invalid section_id: {section_id}")

    logger.debug(f"REFINE: Calling get_section_state(agent_id={AGENT_ID}, section_id={section_id_int}, user_id={user_id})")
    api_result = await dentapp_client.get_section_state(
        agent_id=AGENT_ID,
        section_id=section_id_int,
        user_id=user_id
    )

    if not api_result:
        logger.error("REFINE_ERROR: DentApp API returned no data")
        raise Exception(f"Failed to fetch section data from DentApp API")

    # Extract content from API response
    data = api_result.get('data', {})
    content_obj = data.get('content', {})

    # Handle both string and object formats
    if isinstance(content_obj, str):
        original_content = content_obj
    elif isinstance(content_obj, dict):
        original_content = content_obj.get('text', '')
    else:
        original_content = ''

    if not original_content or not original_content.strip():
        logger.warning(f"REFINE_WARNING: Section {section_id} has no content")
        return {
            "success": False,
            "error": "Section has no content to refine",
            "section_id": section_id
        }

    logger.info(f"REFINE: ✅ Fetched content from database (length: {len(original_content)})")

    # Step 4: Construct refinement prompt with clear structure
    logger.info("REFINE: Step 4/5 - Constructing refinement prompt")
    full_refinement_prompt = f"""## BACKGROUND CONTEXT

The following is the original system prompt that was used to generate this section:

---
{rendered_section_prompt}
---

## CURRENT CONTENT

The user's current section content (generated following the above prompt):

{original_content}

## REFINEMENT TASK

The user wants to refine this content with the following instruction:

"{refinement_prompt}"

Please revise the content according to the user's instruction while:
- Maintaining the section structure and format specified in the original prompt
- Preserving consistency with the context (ICP, Pain points, etc.) mentioned in the background
- Keeping the Value Canvas tone and style
- Only changing what the user explicitly requested

IMPORTANT OUTPUT INSTRUCTIONS:
- Output ONLY the refined content in plain text format
- Do NOT use markdown code blocks (```) or any formatting wrappers
- Do NOT include explanations, meta-commentary, or any text outside the refined content
- Match the exact same format and structure as the original content above
- Your response should be directly usable as the refined section content
"""

    logger.debug(f"REFINE: Constructed prompt (length: {len(full_refinement_prompt)})")

    # Step 5: Call OpenAI LLM to generate refined content
    logger.info("REFINE: Step 5/5 - Calling LLM for refinement")
    llm = get_model()

    # Use non-streaming config
    non_streaming_config = RunnableConfig(
        configurable={"stream": False},
        tags=["refine_operation", "do_not_stream"],
        callbacks=[]
    )

    logger.debug("REFINE: Invoking LLM for refinement...")
    refined_text = await llm.ainvoke(
        full_refinement_prompt,
        config=non_streaming_config
    )

    # Extract text content from LLM response
    if hasattr(refined_text, 'content'):
        refined_plain_text = refined_text.content
    else:
        refined_plain_text = str(refined_text)

    logger.info(f"REFINE: ✅ Successfully refined content (length: {len(refined_plain_text)})")

    # Convert to Tiptap format
    refined_tiptap = plain_text_to_tiptap(refined_plain_text)
    logger.debug("REFINE: Converted refined text to Tiptap format")

    logger.info(f"=== REFINE_SECTION_SUCCESS: section_id={section_id} ===")

    return {
        "success": True,
        "section_id": section_id,
        "user_id": user_id,
        "thread_id": thread_id,
        "refined_content": {
            "plain_text": refined_plain_text,
            "tiptap": refined_tiptap
        },
        "original_content": {
            "plain_text": original_content
        }
    }
