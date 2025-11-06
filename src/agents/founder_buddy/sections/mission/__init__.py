"""Mission section for Founder Buddy."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

MISSION_TEMPLATE = SectionTemplate(
    section_id=SectionID.MISSION,
    name="Mission",
    description="Define your mission, vision, and target audience",
    system_prompt_template="""
You are helping the founder clarify their mission and vision.

In this section, you need to gather:
1. Mission statement - What change are they trying to make in the world?
2. Vision statement - What does success look like in 5-10 years?
3. Target audience - Who are they serving?

Guidelines:
- Ask one question at a time
- Use the founder's own words when possible
- Keep it simple and clear
- Avoid jargon and buzzwords
- Once you have all three elements, present a summary and ask if they're satisfied
""",
    validation_rules=[
        ValidationRule(
            field_name="mission_description",
            rule_type="required",
            value=True,
            error_message="Mission description is required"
        ),
        ValidationRule(
            field_name="vision_statement",
            rule_type="required",
            value=True,
            error_message="Vision statement is required"
        ),
        ValidationRule(
            field_name="target_audience",
            rule_type="required",
            value=True,
            error_message="Target audience is required"
        ),
    ],
    required_fields=["mission_description", "vision_statement", "target_audience"],
    next_section=SectionID.IDEA,
)

