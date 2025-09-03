"""Outcome Prize section models."""

from pydantic import BaseModel, Field


class OutcomePrizeData(BaseModel):
    """Data model for Outcome Prize section."""
    outcome_prize: str | None = Field(None, description="The compelling result they desire")
    compelling_result: str | None = Field(None, description="The specific outcome clients want")
    result_timeframe: str | None = Field(None, description="When clients can expect to see results")
    success_metrics: list[str] | None = Field(None, description="How success is measured")
