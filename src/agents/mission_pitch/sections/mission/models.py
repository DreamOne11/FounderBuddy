"""Mission section models."""

from pydantic import BaseModel, Field


class MissionData(BaseModel):
    """Data model for Mission section."""
    mission_statement: str | None = Field(None, description="The clear, compelling mission statement")
