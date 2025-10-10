"""Data models for the Refinement section."""

from pydantic import BaseModel, Field


class RefinementData(BaseModel):
    """A data structure to hold refinement information."""
    
    pitch_refined: bool = Field(
        False, 
        description="Whether the pitch has been refined and improved"
    )
    refined_pitch: str | None = Field(
        None, 
        description="The refined version of the pitch"
    )
    refinement_iterations: list[str] = Field(
        default_factory=list,
        description="List of refinement iterations made"
    )
    user_satisfied: bool = Field(
        False, 
        description="Whether the user is satisfied with the refined pitch"
    )
    final_feedback: str | None = Field(
        None, 
        description="User's final feedback on the refined pitch"
    )
    ready_for_testing: bool = Field(
        False, 
        description="Whether the pitch is ready for real-world testing"
    )
