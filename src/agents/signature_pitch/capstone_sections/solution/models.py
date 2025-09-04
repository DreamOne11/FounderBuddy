"""CAPSTONE Step 4: SOLUTION section models."""

from pydantic import BaseModel, Field


class SolutionData(BaseModel):
    """Data model for SOLUTION section - Four key solution elements."""

    focus: str | None = Field(None, description="Core of their solution")
    payoffs: str | None = Field(None, description="Benefits and results")
    what_how: str | None = Field(None, description="Unique signature method or system")
    prize: str | None = Field(None, description="Ultimate compelling outcome/transformation")
    signature_method: str | None = Field(None, description="Their unique methodology or framework")
