"""Team & Traction section for Founder Buddy."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

TEAM_TRACTION_TEMPLATE = SectionTemplate(
    section_id=SectionID.TEAM_TRACTION,
    name="Team & Traction",
    description="Describe your team and current progress/traction",
    system_prompt_template="""
You are helping the founder describe their team and traction.

In this section, you need to gather:
1. Team members - Who is on the team? What are their roles and backgrounds?
2. Key milestones - What have you achieved so far?
3. Traction metrics - What data do you have? (users, revenue, growth, etc.)

Guidelines:
- Ask one question at a time
- Focus on relevant experience and achievements
- Be specific about metrics and milestones
- Help them articulate their progress clearly
- Once you have all elements, present a summary and ask if they're satisfied
""",
    validation_rules=[
        ValidationRule(
            field_name="team_members",
            rule_type="required",
            value=True,
            error_message="Team information is required"
        ),
    ],
    required_fields=["team_members"],
    next_section=SectionID.INVEST_PLAN,
)

