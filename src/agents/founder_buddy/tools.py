"""Tools for Founder Buddy Agent."""

import logging
import re
from typing import Any

from langchain_core.tools import tool

from core.settings import settings
from integrations.supabase.supabase_client import SupabaseClient

from .enums import SectionID, SectionStatus
from .prompts import BASE_RULES, SECTION_TEMPLATES

logger = logging.getLogger(__name__)

# Founder Buddy uses agent ID "founder-buddy"
FOUNDER_BUDDY_AGENT_ID = "founder-buddy"


@tool
async def get_context(
    user_id: int,
    thread_id: str,
    section_id: str,
    founder_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Get context packet for a specific Founder Buddy section.
    
    This tool fetches section data from the database and generates
    the appropriate system prompt based on the section template.
    
    Args:
        user_id: Integer user ID from frontend
        thread_id: Thread identifier
        section_id: Section identifier (e.g., 'mission', 'idea')
        founder_data: Current founder data for template rendering
    
    Returns:
        Context packet with system prompt and draft content
    """
    logger.info("=== DATABASE_DEBUG: get_context() ENTRY ===")
    logger.info(f"DATABASE_DEBUG: Section: {section_id}, User: {user_id}, Thread: {thread_id}")
    logger.debug(f"DATABASE_DEBUG: User ID type: {type(user_id)}, Thread ID type: {type(thread_id)}")
    logger.debug(f"DATABASE_DEBUG: Founder data provided: {bool(founder_data)}")
    
    # Get section template
    template = SECTION_TEMPLATES.get(section_id)
    if not template:
        raise ValueError(f"Unknown section ID: {section_id}")
    
    # Generate system prompt
    base_prompt = BASE_RULES
    section_prompt = template.system_prompt_template
    
    # Render template with founder_data if provided
    if founder_data is None:
        founder_data = {}
    
    # Allow partial rendering: missing keys will be replaced with empty string
    def _replace_placeholder(match):
        key = match.group(1)
        return str(founder_data.get(key, "")) if isinstance(founder_data, dict) else ""
    
    # Only replace simple placeholders like {identifier}, keep other braces unchanged
    section_prompt = re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", _replace_placeholder, section_prompt)
    
    system_prompt = f"{base_prompt}\n\n---\n\n{section_prompt}"
    
    # Fetch draft from database
    logger.debug("DATABASE_DEBUG: Starting database fetch for existing section state...")
    draft = None
    status = SectionStatus.PENDING.value
    
    # Try Supabase API if configured
    if hasattr(settings, 'SUPABASE_URL') and settings.SUPABASE_URL:
        logger.info("=== TOOLS_API_CALL: get_context() using Supabase ===")
        logger.info(f"TOOLS_API_CALL: section_id='{section_id}', user_id='{user_id}', thread_id='{thread_id}'")
        try:
            client = SupabaseClient()
            
            # Get section state from Supabase
            result = client.client.table("section_states")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("thread_id", thread_id)\
                .eq("agent_id", FOUNDER_BUDDY_AGENT_ID)\
                .eq("section_id", section_id)\
                .maybe_single()\
                .execute()
            
            if result.data:
                logger.info(f"TOOLS_API_CALL: ✅ Found existing data for section {section_id}")
                logger.debug(f"TOOLS_API_CALL: Content preview: {str(result.data.get('content', ''))[:200]}...")
                
                # Create draft content from database response
                content_data = result.data.get("content")
                if content_data:
                    draft = {
                        "content": content_data,
                        "plain_text": result.data.get("plain_text"),
                    }
                
                # Determine status
                db_status = result.data.get("status", "pending")
                if db_status in ["done", "in_progress", "pending"]:
                    status = db_status
                else:
                    # Fallback: determine from content
                    if content_data:
                        status = SectionStatus.IN_PROGRESS.value
                    else:
                        status = SectionStatus.PENDING.value
                    
                logger.info(f"TOOLS_API_CALL: Status determined: {status}")
            else:
                logger.info(f"TOOLS_API_CALL: ✅ No existing data for section {section_id}")
                
        except Exception as e:
            logger.error(f"TOOLS_API_CALL: ❌ Supabase error in get_context: {e}")
            # Continue without data (will use defaults)
            pass
    
    logger.info(f"DATABASE_DEBUG: Final status: {status}, draft: {bool(draft)}")
    logger.info("=== DATABASE_DEBUG: get_context() EXIT ===")
    
    # Validate section_id (but return as string for Pydantic to convert)
    try:
        SectionID(section_id)
    except ValueError:
        logger.error(f"Invalid section_id: {section_id}")
        raise ValueError(f"Unknown section ID: {section_id}")
    
    # Validate status (but return as string for Pydantic to convert)
    if status not in [s.value for s in SectionStatus]:
        logger.warning(f"Invalid status: {status}, defaulting to PENDING")
        status = SectionStatus.PENDING.value
    
    # Return dict with string values - Pydantic will convert to enums
    # draft should be a dict with 'content' (Tiptap JSON) and optionally 'plain_text'
    return {
        "section_id": section_id,
        "status": status,
        "system_prompt": system_prompt,
        "draft": draft,
        "validation_rules": {str(i): rule.model_dump() for i, rule in enumerate(getattr(template, "validation_rules", []))},
    }


__all__ = [
    "get_context",
]

