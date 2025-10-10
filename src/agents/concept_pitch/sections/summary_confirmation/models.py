"""Data models for the Summary Confirmation section."""

from pydantic import BaseModel, Field


class SummaryConfirmationData(BaseModel):
    """A data structure to hold summary confirmation information."""
    
    summary_confirmed: bool = Field(
        False, 
        description="Whether the user has confirmed the summary is accurate"
    )
    summary_text: str | None = Field(
        None, 
        description="The confirmed summary text"
    )
    corrections_made: list[str] = Field(
        default_factory=list,
        description="List of corrections made to the summary"
    )
    user_feedback: str | None = Field(
        None, 
        description="User's feedback on the summary"
    )
