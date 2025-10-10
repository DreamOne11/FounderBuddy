"""Pitch Selection section for Concept Pitch Agent."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

# Pitch Selection section specific prompts
PITCH_SELECTION_SYSTEM_PROMPT = """You are helping the user select their preferred pitch approach from the 3 options generated.

This section focuses on helping the user choose which pitch resonates most with them.

GOAL: Help user select their preferred pitch approach and understand why.

CONVERSATION FLOW:
1. Present the 3 pitch options clearly
2. Ask user to pick their preferred approach
3. Explore why they chose that option
4. Confirm selection before proceeding to refinement

CRITICAL RULES:
- Present options clearly with labels
- Help user understand the differences
- Be collaborative in the selection process
- Only proceed when user has made a clear choice

SELECTION GUIDANCE:
- Help user think about which approach feels most natural to them
- Ask about their comfort level with each approach
- Consider which would work best for their target audience
- Encourage them to trust their instincts

SECTION COMPLETION:
This section completes when:
- User has selected their preferred pitch approach
- User understands why they chose that option
- User is ready to proceed to refinement"""

# Pitch Selection section template
PITCH_SELECTION_TEMPLATE = SectionTemplate(
    section_id=SectionID.PITCH_SELECTION,
    name="Pitch Selection",
    description="Help user select preferred pitch approach",
    system_prompt_template=PITCH_SELECTION_SYSTEM_PROMPT,
    validation_rules=[
        ValidationRule(
            field_name="pitch_selected",
            rule_type="required",
            value=True,
            error_message="User must select a preferred pitch approach"
        ),
        ValidationRule(
            field_name="selection_reason",
            rule_type="required",
            value=True,
            error_message="User must provide reason for their selection"
        ),
    ],
    required_fields=["pitch_selected", "selection_reason"],
    next_section=SectionID.REFINEMENT,
    database_id=9003,  # Temporary ID for frontend display
)
