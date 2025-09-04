"""CAPSTONE Step 8: ESSENCE section models."""

from pydantic import BaseModel, Field


class EssenceData(BaseModel):
    """Data model for ESSENCE section - Lasting impression and value reinforcement."""

    reputation: str | None = Field(None, description="Impression they want to leave behind")
    feeling: str | None = Field(None, description="Emotion they want audience to experience")
    lasting_impression: str | None = Field(None, description="The memorable final thought")
    emotional_impact: str | None = Field(
        None, description="How they want people to feel after the pitch"
    )
