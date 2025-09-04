"""Enumerations for Signature Pitch Agent."""

from enum import Enum


class SectionStatus(str, Enum):
    """Status of a Signature Pitch section."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""

    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SignaturePitchSectionID(str, Enum):
    """CAPSTONE Framework section identifiers - 8 Steps for Signature Pitch development."""

    # CAPSTONE Framework - 8 Steps
    CLARITY = "clarity"  # Step 1: Define what they do (Name-Same-Fame)
    AUTHORITY = "authority"  # Step 2: Why should I listen? (4 pillars)
    PROBLEM = "problem"  # Step 3: Articulate audience problems (Context + 3 problems)
    SOLUTION = "solution"  # Step 4: Present unique solution (Focus + Payoffs + What/How + Prize)
    THE_WHY = "the_why"  # Step 5: Connect emotionally (Origin + Mission + Vision)
    OPPORTUNITY = (
        "opportunity"  # Step 6: Transition to partnership (Proposal + Wedding + Honeymoon)
    )
    NEXT_STEPS = "next_steps"  # Step 7: Clear call to action
    ESSENCE = "essence"  # Step 8: Lasting impression (Reputation + Feeling)

    # Implementation/Export
    IMPLEMENTATION = "implementation"

    # Legacy sections (kept for backward compatibility during transition)
    ACTIVE_CHANGE = "active_change"
    SPECIFIC_WHO = "specific_who"
    OUTCOME_PRIZE = "outcome_prize"
    CORE_CREDIBILITY = "core_credibility"
    STORY_SPARK = "story_spark"
    SIGNATURE_LINE = "signature_line"

