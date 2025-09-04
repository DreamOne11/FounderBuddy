"""Prompts and templates for Special Report 7-Step Framework.

This module provides access to the complete 7-Step framework templates
imported from framework_templates.py.
"""

from typing import Any

from .enums import SectionStatus, SpecialReportSection
from .framework_templates import (
    FRAMEWORK_TEMPLATES,
    get_framework_progress_info,
    get_framework_section_order,
)

# Import the 7-Step framework templates
SECTION_TEMPLATES = FRAMEWORK_TEMPLATES


def get_progress_info(section_states: dict[str, Any]) -> dict[str, Any]:
    """Get progress information for 7-Step framework completion."""
    return get_framework_progress_info(section_states)


def get_section_order() -> list[SpecialReportSection]:
    """Get the ordered list of 7-Step framework sections."""
    return get_framework_section_order()


def get_next_section(current_section: SpecialReportSection) -> SpecialReportSection | None:
    """Get the next section in the 7-Step framework flow."""
    order = get_section_order()
    try:
        current_index = order.index(current_section)
        if current_index < len(order) - 1:
            return order[current_index + 1]
    except ValueError:
        pass
    return None


def get_next_unfinished_section(section_states: dict[str, Any]) -> SpecialReportSection | None:
    """Find the next section that should be worked on based on 7-Step sequential progression."""
    order = get_section_order()

    # Find the last completed section
    last_completed_index = -1
    for i, section in enumerate(order):
        state = section_states.get(section.value)
        if state and state.status == SectionStatus.DONE:
            last_completed_index = i
        else:
            # Stop at first non-completed section - don't skip ahead
            break

    # Return the next section after the last completed one
    next_index = last_completed_index + 1
    if next_index < len(order):
        return order[next_index]

    return None


# Legacy compatibility exports for backward compatibility during transition
SECTION_PROMPTS = {
    "base_rules": """This agent now uses the 7-Step Special Report Framework. Please see framework_templates.py for the complete 7-step framework."""
}

# Export the main template access for the agent
__all__ = [
    "SECTION_TEMPLATES",
    "get_progress_info",
    "get_section_order",
    "get_next_section",
    "get_next_unfinished_section",
    "SECTION_PROMPTS",  # Legacy compatibility
]
