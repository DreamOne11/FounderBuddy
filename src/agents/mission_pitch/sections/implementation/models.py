"""Implementation section models."""

from pydantic import BaseModel, Field


class ImplementationData(BaseModel):
    """Data model for Implementation section."""
    complete_pitch: str | None = Field(None, description="The complete 90-second Mission Pitch")
    pitch_confidence: int | None = Field(None, ge=0, le=5, description="User's confidence in their complete pitch")
