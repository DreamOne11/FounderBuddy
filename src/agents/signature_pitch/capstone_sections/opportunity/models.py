"""CAPSTONE Step 6: OPPORTUNITY section models."""

from pydantic import BaseModel, Field


class OpportunityData(BaseModel):
    """Data model for OPPORTUNITY section - Partnership invitation framework."""

    proposal: str | None = Field(None, description="Initial offer and invitation")
    wedding: str | None = Field(None, description="The decision to collaborate")
    honeymoon: str | None = Field(None, description="Successful implementation and desired outcome")
    partnership_vision: str | None = Field(None, description="Complete vision of working together")
    collaboration_process: str | None = Field(None, description="How the partnership will unfold")
