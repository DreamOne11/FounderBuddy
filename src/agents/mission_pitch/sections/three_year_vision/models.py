"""Three Year Vision section models."""

from pydantic import BaseModel, Field
from typing import Dict, Any


class ThreeYearVisionData(BaseModel):
    """Data model for Three Year Vision section."""
    three_year_milestone: str | None = Field(None, description="The specific milestone they'll achieve in 3 years")
    three_year_metrics: Dict[str, Any] | None = Field(None, description="Measurable metrics for the 3-year vision")
