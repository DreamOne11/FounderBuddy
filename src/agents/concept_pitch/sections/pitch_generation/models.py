"""Data models for the Pitch Generation section."""

from pydantic import BaseModel, Field


class PitchGenerationData(BaseModel):
    """A data structure to hold pitch generation information."""
    
    pitch_options_generated: bool = Field(
        False, 
        description="Whether all 3 pitch options have been generated"
    )
    pain_driven_pitch: str | None = Field(
        None, 
        description="The pain-driven pitch option"
    )
    gain_driven_pitch: str | None = Field(
        None, 
        description="The gain-driven pitch option"
    )
    prize_driven_pitch: str | None = Field(
        None, 
        description="The prize-driven pitch option"
    )
    user_selection: str | None = Field(
        None, 
        description="User's selected pitch type (pain, gain, or prize)"
    )
    selection_feedback: str | None = Field(
        None, 
        description="User's feedback on their selection"
    )
