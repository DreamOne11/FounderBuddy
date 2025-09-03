"""Personal Origin section models."""

from pydantic import BaseModel, Field


class PersonalOriginData(BaseModel):
    """Data model for Personal Origin section."""
    personal_origin_age: int | None = Field(None, description="Age when the formative experience occurred")
    personal_origin_setting: str | None = Field(None, description="Where the experience took place")
    personal_origin_key_moment: str | None = Field(None, description="The specific moment or experience")
    personal_origin_link_to_theme: str | None = Field(None, description="How this experience connects to their hidden theme")
