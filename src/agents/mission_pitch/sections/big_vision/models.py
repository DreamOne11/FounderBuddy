"""Big Vision section models."""

from pydantic import BaseModel, Field


class BigVisionData(BaseModel):
    """Data model for Big Vision section."""
    big_vision: str | None = Field(None, description="The aspirational long-term vision")
    big_vision_selfless_test_passed: bool | None = Field(None, description="Whether the vision passes the selfless test")
