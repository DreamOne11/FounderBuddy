"""Framework models for Special Report 7-Step Process.

This module contains the data models for the complete 7-step Special Report framework
that complements the existing models.py file.
"""

from typing import Any

from pydantic import BaseModel, Field

from .enums import SectionStatus, SpecialReportSection
from .framework_sections import (
    AttractData,
    DisruptData,
    InformData,
    InviteData,
    OvercomeData,
    RecommendData,
    ReinforceData,
)


class SpecialReportCanvasData(BaseModel):
    """Extended canvas data model for Special Report 7-Step Framework."""

    # Step 1: ATTRACT
    selected_title: str | None = Field(None, description="Final confirmed Special Report title")
    subtitle: str | None = Field(None, description="Compelling subtitle")
    transformation_promise: str | None = Field(None, description="Journey from struggle to prize")

    # Step 2: DISRUPT
    opening_disruption: str | None = Field(None, description="Bold industry disruption statement")
    dominant_problems: list[str] | None = Field(None, description="Three key problems")
    transitional_bridge: str | None = Field(None, description="Problem to solution bridge")

    # Step 3: INFORM
    signature_method: str | None = Field(None, description="User's signature method")
    connection_stories: list[str] | None = Field(None, description="Proof stories")
    logic_frameworks: list[str] | None = Field(None, description="Supporting frameworks")
    big_picture_trends: list[str] | None = Field(None, description="Trends and metaphors")
    three_main_payoffs: list[str] | None = Field(None, description="Key solution benefits")

    # Step 4: RECOMMEND
    directional_shifts: list[str] | None = Field(None, description="Actionable next steps")
    quick_wins: list[str] | None = Field(None, description="Immediate implementable actions")

    # Step 5: OVERCOME
    common_objections: list[str] | None = Field(None, description="Most frequent objections")
    story_responses: list[str] | None = Field(None, description="Story-based responses")
    metaphor_responses: list[str] | None = Field(None, description="Metaphor-based responses")

    # Step 6: REINFORCE
    core_message: str | None = Field(None, description="Central report message")
    main_takeaways: list[str] | None = Field(None, description="Key takeaways")
    memorable_maxim: str | None = Field(None, description="Closing statement")

    # Step 7: INVITE
    desired_next_step: str | None = Field(None, description="Specific desired action")
    vision_statement: str | None = Field(None, description="What's possible for reader")
    call_to_action: str | None = Field(None, description="Clear action instruction")


class FrameworkSectionState(BaseModel):
    """Section state for Special Report framework sections."""

    section_id: SpecialReportSection
    status: SectionStatus = SectionStatus.PENDING
    data: (
        AttractData
        | DisruptData
        | InformData
        | RecommendData
        | OvercomeData
        | ReinforceData
        | InviteData
        | None
    ) = None


def validate_framework_section_completion(section_state: Any) -> bool:
    """Validate if a framework section is properly completed."""
    if not section_state or section_state.status != SectionStatus.DONE:
        return False

    # Add specific validation logic for each section type
    if hasattr(section_state, "data") and section_state.data:
        # Basic validation - at least some data exists
        return True

    return False


def get_framework_completion_summary(section_states: dict[str, Any]) -> dict[str, Any]:
    """Get summary of Special Report framework completion status."""
    framework_sections = [
        SpecialReportSection.ATTRACT,
        SpecialReportSection.DISRUPT,
        SpecialReportSection.INFORM,
        SpecialReportSection.RECOMMEND,
        SpecialReportSection.OVERCOME,
        SpecialReportSection.REINFORCE,
        SpecialReportSection.INVITE,
    ]

    completed_sections = []
    pending_sections = []

    for section in framework_sections:
        section_state = section_states.get(section.value)
        if section_state and validate_framework_section_completion(section_state):
            completed_sections.append(section.value)
        else:
            pending_sections.append(section.value)

    return {
        "framework": "Special Report 7-Step",
        "total_steps": len(framework_sections),
        "completed_steps": len(completed_sections),
        "remaining_steps": len(pending_sections),
        "completion_percentage": round(
            (len(completed_sections) / len(framework_sections)) * 100, 1
        ),
        "completed_sections": completed_sections,
        "pending_sections": pending_sections,
        "is_complete": len(pending_sections) == 0,
    }


def get_framework_section_data_model(section_id: str) -> type[BaseModel]:
    """Get the appropriate data model class for a framework section."""
    section_models = {
        SpecialReportSection.ATTRACT.value: AttractData,
        SpecialReportSection.DISRUPT.value: DisruptData,
        SpecialReportSection.INFORM.value: InformData,
        SpecialReportSection.RECOMMEND.value: RecommendData,
        SpecialReportSection.OVERCOME.value: OvercomeData,
        SpecialReportSection.REINFORCE.value: ReinforceData,
        SpecialReportSection.INVITE.value: InviteData,
    }

    return section_models.get(section_id, BaseModel)
