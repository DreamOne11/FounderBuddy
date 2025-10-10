"""Enumerations for Concept Pitch Agent."""

from enum import Enum


class SectionStatus(str, Enum):
    """Status of a Concept Pitch section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SectionID(str, Enum):
    """Concept Pitch section identifiers."""
    # CAOS Framework Sections
    SUMMARY_CONFIRMATION = "summary_confirmation"  # Confirm idea summary from Value Canvas
    PITCH_GENERATION = "pitch_generation"          # Generate 3 pitch options
    PITCH_SELECTION = "pitch_selection"            # User selects preferred pitch
    REFINEMENT = "refinement"                      # Refine selected pitch
    IMPLEMENTATION = "implementation"              # Save final pitch
