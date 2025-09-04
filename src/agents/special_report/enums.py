"""Enums for Special Report Agent."""

from enum import Enum


class RouterDirective(str, Enum):
    """Router directive for state transitions."""

    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SpecialReportSection(str, Enum):
    """Special Report section identifiers."""

    # New 7-Step Framework sections
    ATTRACT = "attract"
    DISRUPT = "disrupt"
    INFORM = "inform"
    RECOMMEND = "recommend"
    OVERCOME = "overcome"
    REINFORCE = "reinforce"
    INVITE = "invite"

    # Implementation/Export section
    IMPLEMENTATION = "implementation"


class SectionStatus(str, Enum):
    """Section completion status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
