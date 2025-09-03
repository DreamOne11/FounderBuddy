"""Specific Who section models."""

from pydantic import BaseModel, Field


class SpecificWhoData(BaseModel):
    """Data model for Specific Who section."""
    specific_who: str | None = Field(None, description="The exact audience they serve")
    target_audience: str | None = Field(None, description="Detailed description of their ideal client")
    audience_characteristics: list[str] | None = Field(None, description="Key characteristics of their audience")
    audience_pain_points: list[str] | None = Field(None, description="Main challenges their audience faces")
