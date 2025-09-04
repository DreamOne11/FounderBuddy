"""Step 7: INVITE section models."""

from pydantic import BaseModel, Field


class InviteData(BaseModel):
    """Data model for INVITE section - Call to action and vision casting."""

    desired_next_step: str | None = Field(None, description="Specific action desired from reader")
    smooth_transition: str | None = Field(None, description="Natural bridge from content to action")
    vision_statement: str | None = Field(None, description="What's possible for the reader")
    call_to_action: str | None = Field(
        None, description="Clear, specific instruction for next step"
    )
    urgency_element: str | None = Field(None, description="Motivating factor to act now")
