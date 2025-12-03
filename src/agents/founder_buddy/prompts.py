"""Founder Buddy Agent - System prompt and section templates."""

from .enums import SectionID, SectionStatus
from .sections import BASE_RULES, SECTION_TEMPLATES


def get_next_section(current_section: SectionID) -> SectionID | None:
    """Get the next section in sequence."""
    section_order = [
        SectionID.MISSION,
        SectionID.IDEA,
        SectionID.TEAM_TRACTION,
        SectionID.INVEST_PLAN,
    ]
    
    try:
        current_index = section_order.index(current_section)
        if current_index < len(section_order) - 1:
            return section_order[current_index + 1]
    except ValueError:
        pass
    
    return None


def get_next_unfinished_section(state: dict) -> SectionID | None:
    """Get the next unfinished section."""
    section_order = [
        SectionID.MISSION,
        SectionID.IDEA,
        SectionID.TEAM_TRACTION,
        SectionID.INVEST_PLAN,
    ]
    
    section_states = state.get("section_states", {})
    current_section = state.get("current_section")
    
    # Find the first unfinished section
    for section_id in section_order:
        section_state = section_states.get(section_id.value)
        if section_state and section_state.get("status") == SectionStatus.DONE:
            continue
        return section_id
    
    return None


__all__ = [
    "BASE_RULES",
    "SECTION_TEMPLATES",
    "get_next_section",
    "get_next_unfinished_section",
]


