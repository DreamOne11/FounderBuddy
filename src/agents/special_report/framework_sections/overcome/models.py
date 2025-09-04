"""Step 5: OVERCOME section models."""

from pydantic import BaseModel, Field


class OvercomeData(BaseModel):
    """Data model for OVERCOME section - Objection handling and confidence building."""

    common_objections: list[str] | None = Field(
        None, description="Most frequent objections from prospects"
    )
    story_responses: list[str] | None = Field(
        None, description="Connection-based responses using stories"
    )
    metaphor_responses: list[str] | None = Field(
        None, description="Big Picture responses using metaphors"
    )
    unasked_questions: list[str] | None = Field(
        None, description="Questions readers have but don't voice"
    )
    confidence_builders: list[str] | None = Field(
        None, description="Evidence that builds confidence in approach"
    )
