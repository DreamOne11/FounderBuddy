"""Enumerations for Founder Buddy Agent."""

from enum import Enum


class SectionStatus(str, Enum):
    """Status of a Founder Buddy section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SectionID(str, Enum):
    """Founder Buddy section identifiers."""
    MISSION = "mission"              # Section 1: Mission/Vision
    IDEA = "idea"                    # Section 2: Core Idea/Product
    TEAM_TRACTION = "team_traction"  # Section 3: Team & Traction
    INVEST_PLAN = "invest_plan"      # Section 4: Investment Plan

