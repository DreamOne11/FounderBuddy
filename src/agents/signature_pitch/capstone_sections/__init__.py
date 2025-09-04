"""CAPSTONE Framework sections for Signature Pitch Agent."""

# Import section-specific models and prompts following the established pattern
from .authority import AUTHORITY_PROMPTS, AuthorityData
from .clarity import CLARITY_PROMPTS, ClarityData
from .essence import ESSENCE_PROMPTS, EssenceData
from .next_steps import NEXT_STEPS_PROMPTS, NextStepsData
from .opportunity import OPPORTUNITY_PROMPTS, OpportunityData
from .problem import PROBLEM_PROMPTS, ProblemData
from .solution import SOLUTION_PROMPTS, SolutionData
from .the_why import THE_WHY_PROMPTS, TheWhyData

__all__ = [
    # Data models
    "ClarityData",
    "AuthorityData",
    "ProblemData",
    "SolutionData",
    "TheWhyData",
    "OpportunityData",
    "NextStepsData",
    "EssenceData",
    # Prompt templates
    "CLARITY_PROMPTS",
    "AUTHORITY_PROMPTS",
    "PROBLEM_PROMPTS",
    "SOLUTION_PROMPTS",
    "THE_WHY_PROMPTS",
    "OPPORTUNITY_PROMPTS",
    "NEXT_STEPS_PROMPTS",
    "ESSENCE_PROMPTS",
]
