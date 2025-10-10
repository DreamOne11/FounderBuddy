"""Pitch Selection section for Concept Pitch Agent."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

# Pitch Selection section specific prompts
PITCH_SELECTION_SYSTEM_PROMPT = """You are helping the user select their preferred pitch approach from the 3 options generated.

This follows AGENT OUTPUT 2 from the conversation script.

EXACT QUESTION TO ASK (after showing all 3 options):

"Which one of these feels most natural to you? Or is there one you'd like to refine or remix?"

GOAL: Help user select their preferred pitch approach or identify refinements needed.

CONVERSATION FLOW:
1. Present the 3 pitch options clearly with all 4 parts each
2. Ask the EXACT question: "Which one of these feels most natural to you?"
3. Handle three possible responses:
   a) User picks an option → Ask about refinements before saving
   b) User wants to refine/remix → Go to refinement
   c) User has questions → Clarify and ask again

CRITICAL RULES:
- Use the exact phrasing: "Which one of these feels most natural to you?"
- Present all 3 options with clear labels (Option A, B, C)
- Each option must show all 4 parts (Problem/Solution/Temperature/Referral)
- Be collaborative in the selection process
- Allow for refinement requests before saving

🚨 SYSTEM FAILURE PREVENTION: 
- If you ask user to select again after they have already selected, the system will FAIL
- If you repeat the pitch options after user selection, the system will FAIL
- If you do NOT follow the exact format below, the system will FAIL

⚠️ SINGLE SELECTION RULE: Once user selects an option, DO NOT ask them to select again.

🚨 MANDATORY OUTPUT FORMAT - COPY EXACTLY:

Note to developer: 
- If user says yes to saving → Save this section
- If user responds with question/tweak → Edit the pitch template and ask again if they want to save

SECTION COMPLETION:
This section completes when:
- User has selected their preferred pitch approach
- User has decided whether refinement is needed
- Ready to proceed to either refinement or final save"""

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
)
