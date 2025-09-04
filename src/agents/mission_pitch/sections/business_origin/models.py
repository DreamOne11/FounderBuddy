"""Business Origin section models."""

from pydantic import BaseModel, Field


class BusinessOriginData(BaseModel):
    """Data model for Business Origin section."""
    business_origin_pattern: str | None = Field(None, description="The recurring pattern they noticed in their professional life")
    business_origin_story: str | None = Field(None, description="The specific moment they realized 'this should be a business'")
    business_origin_evidence: str | None = Field(None, description="The proof/validation that convinced them there was a real opportunity")
