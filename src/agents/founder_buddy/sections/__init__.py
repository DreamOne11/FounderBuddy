"""Founder Buddy sections module - aggregates all section templates and prompts."""

from typing import Any

from .base_prompt import BASE_PROMPTS, BASE_RULES
from .mission.__init__ import MISSION_TEMPLATE
from .idea.__init__ import IDEA_TEMPLATE
from .team_traction.__init__ import TEAM_TRACTION_TEMPLATE
from .invest_plan.__init__ import INVEST_PLAN_TEMPLATE

# Aggregate all section templates
SECTION_TEMPLATES: dict[str, Any] = {
    MISSION_TEMPLATE.section_id.value: MISSION_TEMPLATE,
    IDEA_TEMPLATE.section_id.value: IDEA_TEMPLATE,
    TEAM_TRACTION_TEMPLATE.section_id.value: TEAM_TRACTION_TEMPLATE,
    INVEST_PLAN_TEMPLATE.section_id.value: INVEST_PLAN_TEMPLATE,
}

__all__ = [
    "BASE_RULES",
    "BASE_PROMPTS",
    "SECTION_TEMPLATES",
    "MISSION_TEMPLATE",
    "IDEA_TEMPLATE",
    "TEAM_TRACTION_TEMPLATE",
    "INVEST_PLAN_TEMPLATE",
]

