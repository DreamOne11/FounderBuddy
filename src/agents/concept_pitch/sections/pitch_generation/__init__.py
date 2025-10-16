"""Pitch Generation section for Concept Pitch Agent."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

# Pitch Generation section specific prompts - import from prompts.py
from .prompts import PITCH_GENERATION_SYSTEM_PROMPT

# Pitch Generation section template
PITCH_GENERATION_TEMPLATE = SectionTemplate(
    section_id=SectionID.PITCH_GENERATION,
    name="Pitch Generation",
    description="Generate 3 pitch options for user selection",
    system_prompt_template=PITCH_GENERATION_SYSTEM_PROMPT,
    validation_rules=[
        ValidationRule(
            field_name="pitch_options_generated",
            rule_type="required",
            value=True,
            error_message="All 3 pitch options must be generated"
        ),
        ValidationRule(
            field_name="user_selection",
            rule_type="required",
            value=True,
            error_message="User must select a preferred option"
        ),
    ],
    required_fields=["pitch_options_generated", "user_selection"],
    next_section=SectionID.PITCH_SELECTION,
    database_id=9002,  # Temporary ID for frontend display
)
