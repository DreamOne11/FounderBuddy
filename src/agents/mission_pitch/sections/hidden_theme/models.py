"""Hidden Theme section models."""

from pydantic import BaseModel, Field


class HiddenThemeData(BaseModel):
    """Data model for Hidden Theme section."""
    theme_rant: str | None = Field(None, description="The user's passionate explanation of their recurring life pattern")
    theme_1sentence: str | None = Field(None, description="The 1-sentence distillation of their hidden theme")
    theme_confidence: int | None = Field(None, ge=0, le=5, description="User's confidence in the theme (0-5 scale)")
