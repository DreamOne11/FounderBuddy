"""Step 3: INFORM section models."""

from pydantic import BaseModel, Field


class InformData(BaseModel):
    """Data model for INFORM section - Signature method explanation and proof."""

    signature_method: str | None = Field(
        None, description="User's signature method and core principles"
    )
    connection_stories: list[str] | None = Field(
        None, description="Personal or client stories that prove expertise"
    )
    logic_frameworks: list[str] | None = Field(
        None, description="Process models, before/after comparisons, data points"
    )
    big_picture_trends: list[str] | None = Field(
        None, description="Relevant trends and memorable maxims or metaphors"
    )
    three_main_payoffs: list[str] | None = Field(
        None, description="Three key benefits of their solution"
    )
    proof_points: list[str] | None = Field(None, description="Supporting data and evidence")
