"""Step 1: ATTRACT section models."""

from pydantic import BaseModel, Field


class AttractData(BaseModel):
    """Data model for ATTRACT section - Compelling topic creation."""

    topic_options: list[str] | None = Field(
        None, description="Generated topic options for selection"
    )
    selected_title: str | None = Field(None, description="Final confirmed Special Report title")
    subtitle: str | None = Field(
        None, description="Compelling subtitle that supports the main title"
    )
    transformation_promise: str | None = Field(
        None, description="Clear journey from struggle to prize"
    )
    bookstore_test_notes: str | None = Field(
        None, description="Why this topic passes the bookstore test"
    )
