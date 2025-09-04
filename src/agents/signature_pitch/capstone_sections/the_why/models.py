"""CAPSTONE Step 5: THE WHY section models."""

from pydantic import BaseModel, Field


class TheWhyData(BaseModel):
    """Data model for THE WHY section - Personal motivation and purpose."""

    origin: str | None = Field(None, description="Story of how they began this journey")
    mission: str | None = Field(None, description="Their purpose and what they do")
    vision: str | None = Field(None, description="Long-term view and ultimate goal")
    personal_story: str | None = Field(None, description="The compelling personal narrative")
    deeper_purpose: str | None = Field(None, description="What truly drives them")
