"""Step 4: RECOMMEND section models."""

from pydantic import BaseModel, Field


class RecommendData(BaseModel):
    """Data model for RECOMMEND section - Actionable advice for trust building."""

    directional_shifts: list[str] | None = Field(
        None, description="1-3 simple, actionable next steps"
    )
    quick_wins: list[str] | None = Field(None, description="Immediate implementable actions")
    practical_steps: list[str] | None = Field(
        None, description="Specific steps readers can take now"
    )
    trust_builders: list[str] | None = Field(
        None, description="Actions that demonstrate immediate value"
    )
    connection_to_method: str | None = Field(
        None, description="How recommendations connect to larger solution"
    )
