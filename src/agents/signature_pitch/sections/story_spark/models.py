"""Story Spark section models."""

from pydantic import BaseModel, Field


class StorySparkData(BaseModel):
    """Data model for Story Spark section."""
    story_spark: str | None = Field(None, description="The short narrative hook or example")
    narrative_hook: str | None = Field(None, description="The compelling story element that captures attention")
    story_outcome: str | None = Field(None, description="The result or transformation shown in the story")
    story_relevance: str | None = Field(None, description="How the story connects to the audience's situation")
