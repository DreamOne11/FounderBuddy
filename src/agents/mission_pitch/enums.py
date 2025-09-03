"""Enumerations for Mission Pitch Agent."""

from enum import Enum


class SectionStatus(str, Enum):
    """Status of a Mission Pitch section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class MissionSectionID(str, Enum):
    """Mission Pitch section identifiers."""
    # The 6 core Mission Pitch components
    HIDDEN_THEME = "hidden_theme"           # 1-sentence recurring life pattern
    PERSONAL_ORIGIN = "personal_origin"     # Early memory that shaped worldview
    BUSINESS_ORIGIN = "business_origin"     # "This should be a business" moment
    MISSION = "mission"                     # Clear change statement for whom
    THREE_YEAR_VISION = "three_year_vision" # Believable exciting milestone
    BIG_VISION = "big_vision"              # Aspirational future passing Selfless Test

    # Implementation/Export
    IMPLEMENTATION = "implementation"
