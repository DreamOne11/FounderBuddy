from enum import Enum
from typing import Optional
from pydantic import BaseModel


class MissionPitchStep(Enum):
    """Enum for Mission Pitch workflow steps"""
    HIDDEN_THEME = "hidden_theme"
    PERSONAL_ORIGIN = "personal_origin"
    BUSINESS_ORIGIN = "business_origin"
    MISSION = "mission"
    THREE_YEAR_VISION = "three_year_vision"
    BIG_VISION = "big_vision"
    COMPLETE = "complete"


class BrandArchetype(Enum):
    """Brand archetypes for leadership positioning"""
    CHALLENGER = "challenger"
    MAGICIAN = "magician"
    HERO = "hero"
    EXPLORER = "explorer"
    SAGE = "sage"
    CREATOR = "creator"
    CAREGIVER = "caregiver"
    RULER = "ruler"


class MissionPitchData(BaseModel):
    """Data structure for storing Mission Pitch progress"""
    current_step: MissionPitchStep = MissionPitchStep.HIDDEN_THEME
    
    # Step 1: Hidden Theme
    theme_rant: Optional[str] = None
    distilled_theme: Optional[str] = None
    theme_confidence: Optional[int] = None
    
    # Step 2: Personal Origin
    personal_origin_story: Optional[str] = None
    origin_satisfaction: Optional[int] = None
    identified_archetype: Optional[BrandArchetype] = None
    
    # Step 3: Business Origin
    business_origin_story: Optional[str] = None
    business_satisfaction: Optional[int] = None
    
    # Step 4: Mission
    mission_statement: Optional[str] = None
    mission_alignment: Optional[int] = None
    
    # Step 5: 3-Year Vision
    three_year_vision: Optional[str] = None
    vision_satisfaction: Optional[int] = None
    
    # Step 6: Big Vision
    big_vision: Optional[str] = None
    big_vision_satisfaction: Optional[int] = None
    selfless_test_passed: Optional[bool] = None
    
    # Overall completion
    complete_story_satisfaction: Optional[int] = None
    ready_for_testing: bool = False