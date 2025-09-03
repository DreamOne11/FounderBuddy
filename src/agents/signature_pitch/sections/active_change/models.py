"""Active Change section models."""

from pydantic import BaseModel, Field


class ActiveChangeData(BaseModel):
    """Data model for Active Change section."""
    active_change: str | None = Field(None, description="The transformation the user creates in the world")
    transformation_type: str | None = Field(None, description="The type of change or transformation")
    impact_area: str | None = Field(None, description="The area or domain where the change occurs")
