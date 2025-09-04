"""CAPSTONE Step 2: AUTHORITY section models."""

from pydantic import BaseModel, Field


class AuthorityData(BaseModel):
    """Data model for AUTHORITY section - Four pillars of credibility."""

    experience: str | None = Field(None, description="Formal credentials and real-world experience")
    associations: str | None = Field(
        None, description="Notable people, brands, or media connections"
    )
    accolades: str | None = Field(None, description="Awards, rankings, praise")
    results: str | None = Field(None, description="Measurable outcomes achieved")
    authority_pillars: str | None = Field(
        None, description="Selected 1-2 strongest authority pillars"
    )
