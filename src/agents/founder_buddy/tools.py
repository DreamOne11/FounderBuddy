"""Tools for Founder Buddy Agent."""

import logging
from typing import Any

from langchain_core.tools import tool

from .enums import SectionID, SectionStatus
from .sections import SECTION_TEMPLATES

logger = logging.getLogger(__name__)


@tool
async def get_context(user_id: int, thread_id: str | None, section_id: str, founder_data: dict) -> dict:
    """
    Get context for a specific Founder Buddy section.
    
    Args:
        user_id: Integer user ID from frontend
        thread_id: Thread identifier (can be None for new conversations)
        section_id: Section identifier (e.g., 'mission', 'idea', 'team_traction', 'invest_plan')
        founder_data: Current founder data for template rendering
    
    Returns:
        Context packet with system prompt
    """
    logger.info(f"GET_CONTEXT: Section: {section_id}, User: {user_id}, Thread: {thread_id or 'None'}")
    
    # Get section-specific system prompt from template
    section_template = SECTION_TEMPLATES.get(section_id)
    if section_template:
        system_prompt = section_template.system_prompt_template
        
        # Add BASE_RULES at the beginning
        from .sections import BASE_RULES
        system_prompt = BASE_RULES + "\n\n" + system_prompt
        
        logger.info(f"GET_CONTEXT: ✅ Using section template for {section_id}")
    else:
        logger.warning(f"GET_CONTEXT: ⚠️ No section template found for {section_id}")
        system_prompt = f"System prompt for {section_id}"
    
    # Initialize context
    context = {
        "section_id": section_id,
        "status": SectionStatus.PENDING.value,
        "system_prompt": system_prompt,
        "draft": None,
        "validation_rules": None,
    }
    
    logger.info(f"GET_CONTEXT: ✅ Returning context for {section_id}")
    return context

