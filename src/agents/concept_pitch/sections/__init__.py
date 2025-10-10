"""Concept Pitch sections module - aggregates all section templates and prompts."""

from typing import Any, Dict

# Import all section templates and prompts
from .base_prompt import BASE_PROMPTS, BASE_RULES
from .summary_confirmation import SUMMARY_CONFIRMATION_TEMPLATE
from .pitch_generation import PITCH_GENERATION_TEMPLATE
from .pitch_selection import PITCH_SELECTION_TEMPLATE
from .refinement import REFINEMENT_TEMPLATE

# Aggregate all section templates
SECTION_TEMPLATES: dict[str, Any] = {
    SUMMARY_CONFIRMATION_TEMPLATE.section_id.value: SUMMARY_CONFIRMATION_TEMPLATE,
    PITCH_GENERATION_TEMPLATE.section_id.value: PITCH_GENERATION_TEMPLATE,
    PITCH_SELECTION_TEMPLATE.section_id.value: PITCH_SELECTION_TEMPLATE,
    REFINEMENT_TEMPLATE.section_id.value: REFINEMENT_TEMPLATE,
}

# Export BASE_RULES directly (previously wrapped in SECTION_PROMPTS dict)
# The SECTION_PROMPTS dict was removed as it only contained one key
# and the name was misleading (it contained base rules, not section prompts)

__all__ = [
    "BASE_RULES",
    "BASE_PROMPTS",
    "SECTION_TEMPLATES",
    "SUMMARY_CONFIRMATION_TEMPLATE",
    "PITCH_GENERATION_TEMPLATE",
    "PITCH_SELECTION_TEMPLATE",
    "REFINEMENT_TEMPLATE",
]
