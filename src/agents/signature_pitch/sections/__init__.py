"""Signature Pitch sections package."""

# Import section-specific models and prompts
from .active_change import ACTIVE_CHANGE_PROMPTS, ActiveChangeData
from .core_credibility import CORE_CREDIBILITY_PROMPTS, CoreCredibilityData
from .implementation import IMPLEMENTATION_PROMPTS, ImplementationData
from .outcome_prize import OUTCOME_PRIZE_PROMPTS, OutcomePrizeData
from .signature_line import SIGNATURE_LINE_PROMPTS, SignatureLineData
from .specific_who import SPECIFIC_WHO_PROMPTS, SpecificWhoData
from .story_spark import STORY_SPARK_PROMPTS, StorySparkData

__all__ = [
    # Data models
    "ActiveChangeData",
    "SpecificWhoData", 
    "OutcomePrizeData",
    "CoreCredibilityData",
    "StorySparkData",
    "SignatureLineData",
    "ImplementationData",
    # Prompt templates
    "ACTIVE_CHANGE_PROMPTS",
    "SPECIFIC_WHO_PROMPTS",
    "OUTCOME_PRIZE_PROMPTS", 
    "CORE_CREDIBILITY_PROMPTS",
    "STORY_SPARK_PROMPTS",
    "SIGNATURE_LINE_PROMPTS",
    "IMPLEMENTATION_PROMPTS",
]
