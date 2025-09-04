"""CAPSTONE Step 1: CLARITY section models."""

from pydantic import BaseModel, Field


class ClarityData(BaseModel):
    """Data model for CLARITY section - Name-Same-Fame components."""

    name: str | None = Field(None, description="Personal and business identity")
    same: str | None = Field(None, description="Industry category for instant understanding")
    fame: str | None = Field(None, description="What makes them different and worthy of attention")
