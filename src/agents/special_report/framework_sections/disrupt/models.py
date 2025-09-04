"""Step 2: DISRUPT section models."""

from pydantic import BaseModel, Field


class DisruptData(BaseModel):
    """Data model for DISRUPT section - Challenge assumptions and raise stakes."""

    opening_disruption: str | None = Field(
        None, description="Bold statement that exposes industry lie or misconception"
    )
    dominant_problems: list[str] | None = Field(
        None, description="Three key problems from Value Canvas"
    )
    problem_urgency: str | None = Field(
        None, description="Why these problems demand immediate attention"
    )
    transitional_bridge: str | None = Field(
        None, description="Connection from problem to solution readiness"
    )
    emotional_stakes: str | None = Field(
        None, description="What's at risk if problems aren't addressed"
    )
