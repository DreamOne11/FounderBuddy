"""Refinement section for Concept Pitch Agent."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

# Refinement section specific prompts
REFINEMENT_SYSTEM_PROMPT = """You are helping the user refine their selected pitch to make it more compelling and testable.

This section focuses on improving the chosen pitch through iterative feedback and refinement.

GOAL: Refine the selected pitch until the user is confident it's ready for real-world testing.

CONVERSATION FLOW:
1. Present the selected pitch clearly
2. Ask for specific feedback and improvements
3. Iteratively refine based on user input
4. Test different versions and approaches
5. Confirm final version before proceeding

CRITICAL RULES:
- Be collaborative and iterative
- Focus on making the pitch more compelling
- Test different phrasings and approaches
- Only proceed when user is confident

REFINEMENT AREAS:
- Language and tone
- Clarity and flow
- Emotional impact
- Specificity and details
- Call to action

SECTION COMPLETION:
This section completes when:
- User is satisfied with the refined pitch
- Pitch is clear, compelling, and testable
- User is ready to proceed to implementation"""

# Refinement section template
REFINEMENT_TEMPLATE = SectionTemplate(
    section_id=SectionID.REFINEMENT,
    name="Refinement",
    description="Refine selected pitch through iterative feedback",
    system_prompt_template=REFINEMENT_SYSTEM_PROMPT,
    validation_rules=[
        ValidationRule(
            field_name="pitch_refined",
            rule_type="required",
            value=True,
            error_message="Pitch must be refined and improved"
        ),
        ValidationRule(
            field_name="user_satisfied",
            rule_type="required",
            value=True,
            error_message="User must be satisfied with the refined pitch"
        ),
    ],
    required_fields=["pitch_refined", "user_satisfied"],
    next_section=SectionID.IMPLEMENTATION,
    database_id=9004,  # Temporary ID for frontend display
)
