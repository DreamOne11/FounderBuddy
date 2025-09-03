"""Signature Pitch sections package."""

# Import section-specific models and prompts
from .active_change import ActiveChangeData, ACTIVE_CHANGE_PROMPTS
from .specific_who import SpecificWhoData, SPECIFIC_WHO_PROMPTS  
from .outcome_prize import OutcomePrizeData, OUTCOME_PRIZE_PROMPTS
from .core_credibility import CoreCredibilityData, CORE_CREDIBILITY_PROMPTS
from .story_spark import StorySparkData, STORY_SPARK_PROMPTS
from .signature_line import SignatureLineData, SIGNATURE_LINE_PROMPTS
from .implementation import ImplementationData, IMPLEMENTATION_PROMPTS

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
