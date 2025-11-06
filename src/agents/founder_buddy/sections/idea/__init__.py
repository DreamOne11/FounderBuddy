"""Idea section for Founder Buddy."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

IDEA_TEMPLATE = SectionTemplate(
    section_id=SectionID.IDEA,
    name="Idea",
    description="Define your core product idea and value proposition",
    system_prompt_template="""
You are helping the founder clarify their core product idea.

In this section, you need to gather:
1. Product description - What are you building?
2. Core value proposition - What problem does it solve?
3. Key features - What are the main features?
4. Differentiation - What makes it different from existing solutions?

Guidelines:
- Ask one question at a time
- Be specific about the problem being solved
- Focus on benefits, not just features
- Help them articulate what makes their solution unique
- Once you have all elements, present a summary and ask if they're satisfied
""",
    validation_rules=[
        ValidationRule(
            field_name="product_description",
            rule_type="required",
            value=True,
            error_message="Product description is required"
        ),
        ValidationRule(
            field_name="core_value_proposition",
            rule_type="required",
            value=True,
            error_message="Core value proposition is required"
        ),
    ],
    required_fields=["product_description", "core_value_proposition"],
    next_section=SectionID.TEAM_TRACTION,
)

