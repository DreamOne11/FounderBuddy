"""Signature Line section models."""

from pydantic import BaseModel, Field


class SignatureLineData(BaseModel):
    """Data model for Signature Line section."""
    signature_line: str | None = Field(None, description="The concise one-line signature pitch")
    ninety_second_pitch: str | None = Field(None, description="The full 90-second signature pitch")
    pitch_hook: str | None = Field(None, description="The opening hook that captures attention")
    pitch_close: str | None = Field(None, description="The closing line that prompts action")
