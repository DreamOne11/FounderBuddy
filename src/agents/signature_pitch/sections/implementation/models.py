"""Implementation section models."""

from pydantic import BaseModel, Field


class ImplementationData(BaseModel):
    """Data model for Implementation section."""
    complete_pitch: str | None = Field(None, description="The complete integrated signature pitch")
    pitch_confidence: int | None = Field(None, ge=0, le=5, description="User's confidence in their complete pitch")
    delivery_notes: list[str] | None = Field(None, description="Notes on how to deliver the pitch effectively")
    usage_contexts: list[str] | None = Field(None, description="Situations where this pitch would be used")
