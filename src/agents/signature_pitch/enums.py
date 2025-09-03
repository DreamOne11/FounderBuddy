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
    """Signature Pitch section identifiers."""
    # The 6 core Signature Pitch components
    ACTIVE_CHANGE = "active_change"         # The transformation you create
    SPECIFIC_WHO = "specific_who"          # The exact audience you serve
    OUTCOME_PRIZE = "outcome_prize"        # The compelling result they desire
    CORE_CREDIBILITY = "core_credibility"  # Proof you can deliver
    STORY_SPARK = "story_spark"           # A short narrative hook or example
    SIGNATURE_LINE = "signature_line"      # The concise pitch (90 seconds → 1 line)

    # Implementation/Export
    IMPLEMENTATION = "implementation"
