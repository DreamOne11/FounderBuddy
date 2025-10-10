"""Data models for the Pitch Selection section."""

from pydantic import BaseModel, Field


class PitchSelectionData(BaseModel):
    """A data structure to hold pitch selection information."""
    
    pitch_selected: str | None = Field(
        None, 
        description="The selected pitch type (pain, gain, or prize)"
    )
    selection_reason: str | None = Field(
        None, 
        description="User's reason for selecting this pitch approach"
    )
    comfort_level: str | None = Field(
        None, 
        description="User's comfort level with the selected approach"
    )
    target_audience_fit: str | None = Field(
        None, 
        description="How well the selected approach fits their target audience"
    )
    selection_confirmed: bool = Field(
        False, 
        description="Whether the user has confirmed their selection"
    )
