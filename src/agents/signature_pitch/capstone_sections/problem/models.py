"""CAPSTONE Step 3: PROBLEM section models."""

from pydantic import BaseModel, Field


class ProblemData(BaseModel):
    """Data model for PROBLEM section - Context and dominant problems."""

    context: str | None = Field(None, description="Scene setting - why the problem is relevant now")
    dominant_problems: str | None = Field(
        None, description="Three specific pain points, mistakes, or frustrations"
    )
    problem_list: list[str] | None = Field(None, description="Individual problems as a list")
    urgency_context: str | None = Field(None, description="Why this problem is urgent right now")
