"""Step 6: REINFORCE section models."""

from pydantic import BaseModel, Field


class ReinforceData(BaseModel):
    """Data model for REINFORCE section - Summary and lasting impression."""

    core_message: str | None = Field(None, description="Central message of the entire report")
    main_takeaways: list[str] | None = Field(None, description="Key points readers should remember")
    key_principles: list[str] | None = Field(
        None, description="Core principles that guide the approach"
    )
    memorable_maxim: str | None = Field(
        None, description="Closing statement that sticks with readers"
    )
    transformation_reminder: str | None = Field(
        None, description="Reinforcement of the journey from struggle to prize"
    )
