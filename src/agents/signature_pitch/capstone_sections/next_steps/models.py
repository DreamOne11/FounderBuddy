"""CAPSTONE Step 7: NEXT STEPS section models."""

from pydantic import BaseModel, Field


class NextStepsData(BaseModel):
    """Data model for NEXT STEPS section - Clear call to action."""

    call_to_action: str | None = Field(None, description="Specific, actionable instruction")
    action_method: str | None = Field(None, description="How they should take the action")
    contact_method: str | None = Field(None, description="Specific way to get in touch or respond")
    urgency_element: str | None = Field(None, description="Why they should act now")
