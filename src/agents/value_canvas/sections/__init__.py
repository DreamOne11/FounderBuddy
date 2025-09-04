"""Value Canvas sections module - aggregates all section templates and prompts."""

from typing import Any, Dict

# Import all section templates and prompts
from .base_prompt import BASE_PROMPTS, BASE_RULES
from .deep_fear import DEEP_FEAR_PROMPTS, DEEP_FEAR_TEMPLATE
from .icp import ICP_PROMPTS, ICP_TEMPLATE
from .icp_stress_test import ICP_STRESS_TEST_PROMPTS, ICP_STRESS_TEST_TEMPLATE
from .implementation import IMPLEMENTATION_PROMPTS, IMPLEMENTATION_TEMPLATE
from .interview import INTERVIEW_PROMPTS, INTERVIEW_TEMPLATE
from .mistakes import MISTAKES_PROMPTS, MISTAKES_TEMPLATE
from .pain import PAIN_PROMPTS, PAIN_TEMPLATE
from .pain_payoff_symmetry import PAIN_PAYOFF_SYMMETRY_PROMPTS, PAIN_PAYOFF_SYMMETRY_TEMPLATE
from .payoffs import PAYOFFS_PROMPTS, PAYOFFS_TEMPLATE
from .prize import PRIZE_PROMPTS, PRIZE_TEMPLATE
from .signature_method import SIGNATURE_METHOD_PROMPTS, SIGNATURE_METHOD_TEMPLATE

# Aggregate all section templates
SECTION_TEMPLATES: dict[str, Any] = {
    INTERVIEW_TEMPLATE.section_id.value: INTERVIEW_TEMPLATE,
    ICP_TEMPLATE.section_id.value: ICP_TEMPLATE,
    ICP_STRESS_TEST_TEMPLATE.section_id.value: ICP_STRESS_TEST_TEMPLATE,
    PAIN_TEMPLATE.section_id.value: PAIN_TEMPLATE,
    DEEP_FEAR_TEMPLATE.section_id.value: DEEP_FEAR_TEMPLATE,
    PAYOFFS_TEMPLATE.section_id.value: PAYOFFS_TEMPLATE,
    PAIN_PAYOFF_SYMMETRY_TEMPLATE.section_id.value: PAIN_PAYOFF_SYMMETRY_TEMPLATE,
    SIGNATURE_METHOD_TEMPLATE.section_id.value: SIGNATURE_METHOD_TEMPLATE,
    MISTAKES_TEMPLATE.section_id.value: MISTAKES_TEMPLATE,
    PRIZE_TEMPLATE.section_id.value: PRIZE_TEMPLATE,
    IMPLEMENTATION_TEMPLATE.section_id.value: IMPLEMENTATION_TEMPLATE,
}

# Aggregate all section prompts
SECTION_PROMPTS: dict[str, Any] = {
    "base_rules": BASE_RULES,
    "interview": INTERVIEW_PROMPTS,
    "icp": ICP_PROMPTS,
    "icp_stress_test": ICP_STRESS_TEST_PROMPTS,
    "pain": PAIN_PROMPTS,
    "deep_fear": DEEP_FEAR_PROMPTS,
    "payoffs": PAYOFFS_PROMPTS,
    "pain_payoff_symmetry": PAIN_PAYOFF_SYMMETRY_PROMPTS,
    "signature_method": SIGNATURE_METHOD_PROMPTS,
    "mistakes": MISTAKES_PROMPTS,
    "prize": PRIZE_PROMPTS,
    "implementation": IMPLEMENTATION_PROMPTS,
}

__all__ = [
    "BASE_RULES",
    "BASE_PROMPTS",
    "SECTION_TEMPLATES",
    "SECTION_PROMPTS",
    "INTERVIEW_TEMPLATE",
    "ICP_TEMPLATE",
    "PAIN_TEMPLATE",
    "DEEP_FEAR_TEMPLATE",
    "PAYOFFS_TEMPLATE",
    "SIGNATURE_METHOD_TEMPLATE",
    "MISTAKES_TEMPLATE",
    "PRIZE_TEMPLATE",
    "IMPLEMENTATION_TEMPLATE",
]