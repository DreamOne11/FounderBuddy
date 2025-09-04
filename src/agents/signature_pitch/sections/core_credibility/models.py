"""Core Credibility section models."""

from pydantic import BaseModel, Field


class CoreCredibilityData(BaseModel):
    """Data model for Core Credibility section."""
    core_credibility: str | None = Field(None, description="Main credibility statement or proof")
    proof_points: list[str] | None = Field(None, description="Specific evidence that supports credibility")
    credentials: list[str] | None = Field(None, description="Relevant credentials or qualifications")
    results_achieved: list[str] | None = Field(None, description="Specific results or outcomes delivered")
