"""CAPSTONE Framework-specific models for Signature Pitch Agent."""

from typing import Any

from pydantic import BaseModel, Field

from .enums import SectionStatus, SignaturePitchSectionID


class ClarityData(BaseModel):
    """Step 1: CLARITY - Name-Same-Fame components."""

    name: str | None = Field(None, description="Personal and business identity")
    same: str | None = Field(None, description="Industry category for instant understanding")
    fame: str | None = Field(None, description="What makes them different and worthy of attention")


class AuthorityData(BaseModel):
    """Step 2: AUTHORITY - Four pillars of credibility."""

    experience: str | None = Field(None, description="Formal credentials and real-world experience")
    associations: str | None = Field(
        None, description="Notable people, brands, or media connections"
    )
    accolades: str | None = Field(None, description="Awards, rankings, praise")
    results: str | None = Field(None, description="Measurable outcomes achieved")
    authority_pillars: str | None = Field(
        None, description="Selected 1-2 strongest authority pillars"
    )


class ProblemData(BaseModel):
    """Step 3: PROBLEM - Context and dominant problems."""

    context: str | None = Field(None, description="Scene setting - why the problem is relevant now")
    dominant_problems: str | None = Field(
        None, description="Three specific pain points, mistakes, or frustrations"
    )


class SolutionData(BaseModel):
    """Step 4: SOLUTION - Four key solution elements."""

    focus: str | None = Field(None, description="Core of their solution")
    payoffs: str | None = Field(None, description="Benefits and results")
    what_how: str | None = Field(None, description="Unique signature method or system")
    prize: str | None = Field(None, description="Ultimate compelling outcome/transformation")


class TheWhyData(BaseModel):
    """Step 5: THE WHY - Personal motivation and purpose."""

    origin: str | None = Field(None, description="Story of how they began this journey")
    mission: str | None = Field(None, description="Their purpose and what they do")
    vision: str | None = Field(None, description="Long-term view and ultimate goal")


class OpportunityData(BaseModel):
    """Step 6: OPPORTUNITY - Partnership invitation framework."""

    proposal: str | None = Field(None, description="Initial offer and invitation")
    wedding: str | None = Field(None, description="The decision to collaborate")
    honeymoon: str | None = Field(None, description="Successful implementation and desired outcome")


class NextStepsData(BaseModel):
    """Step 7: NEXT STEPS - Clear call to action."""

    call_to_action: str | None = Field(None, description="Specific, actionable instruction")


class EssenceData(BaseModel):
    """Step 8: ESSENCE - Lasting impression and value reinforcement."""

    reputation: str | None = Field(None, description="Impression they want to leave behind")
    feeling: str | None = Field(None, description="Emotion they want audience to experience")


class CapstoneState(BaseModel):
    """Complete CAPSTONE framework state data."""

    clarity: ClarityData = Field(default_factory=ClarityData)
    authority: AuthorityData = Field(default_factory=AuthorityData)
    problem: ProblemData = Field(default_factory=ProblemData)
    solution: SolutionData = Field(default_factory=SolutionData)
    the_why: TheWhyData = Field(default_factory=TheWhyData)
    opportunity: OpportunityData = Field(default_factory=OpportunityData)
    next_steps: NextStepsData = Field(default_factory=NextStepsData)
    essence: EssenceData = Field(default_factory=EssenceData)


class CapstoneSectionState(BaseModel):
    """Section state for CAPSTONE framework sections."""

    section_id: SignaturePitchSectionID
    status: SectionStatus = SectionStatus.PENDING
    data: dict[str, Any] = Field(default_factory=dict)
    score: int | None = Field(None, ge=0, le=5, description="User satisfaction rating 0-5")
    completed_at: str | None = Field(None, description="ISO timestamp when section was completed")

    def update_data(self, field: str, value: Any) -> None:
        """Update a specific data field."""
        self.data[field] = value

    def get_data(self, field: str, default: Any = None) -> Any:
        """Get a specific data field with optional default."""
        return self.data.get(field, default)

    def is_complete(self, required_fields: list[str]) -> bool:
        """Check if section has all required fields completed."""
        return all(self.data.get(field) is not None for field in required_fields)


def get_capstone_section_data_model(section_id: SignaturePitchSectionID) -> type[BaseModel]:
    """Get the appropriate data model for a CAPSTONE section."""
    section_models = {
        SignaturePitchSectionID.CLARITY: ClarityData,
        SignaturePitchSectionID.AUTHORITY: AuthorityData,
        SignaturePitchSectionID.PROBLEM: ProblemData,
        SignaturePitchSectionID.SOLUTION: SolutionData,
        SignaturePitchSectionID.THE_WHY: TheWhyData,
        SignaturePitchSectionID.OPPORTUNITY: OpportunityData,
        SignaturePitchSectionID.NEXT_STEPS: NextStepsData,
        SignaturePitchSectionID.ESSENCE: EssenceData,
    }
    return section_models.get(section_id, BaseModel)


def get_required_fields_for_section(section_id: SignaturePitchSectionID) -> list[str]:
    """Get required fields for each CAPSTONE section."""
    required_fields = {
        SignaturePitchSectionID.CLARITY: ["name", "same", "fame"],
        SignaturePitchSectionID.AUTHORITY: ["authority_pillars"],
        SignaturePitchSectionID.PROBLEM: ["context", "dominant_problems"],
        SignaturePitchSectionID.SOLUTION: ["focus", "payoffs", "what_how", "prize"],
        SignaturePitchSectionID.THE_WHY: ["origin", "mission", "vision"],
        SignaturePitchSectionID.OPPORTUNITY: ["proposal", "wedding", "honeymoon"],
        SignaturePitchSectionID.NEXT_STEPS: ["call_to_action"],
        SignaturePitchSectionID.ESSENCE: ["reputation", "feeling"],
        SignaturePitchSectionID.IMPLEMENTATION: [],
    }
    return required_fields.get(section_id, [])


def validate_capstone_section_completion(section_state: CapstoneSectionState) -> bool:
    """Validate that a CAPSTONE section has all required data and is marked complete."""
    if section_state.status != SectionStatus.DONE:
        return False

    required_fields = get_required_fields_for_section(section_state.section_id)
    return section_state.is_complete(required_fields)


def get_capstone_completion_summary(
    section_states: dict[str, CapstoneSectionState],
) -> dict[str, Any]:
    """Get summary of CAPSTONE framework completion status."""
    capstone_sections = [
        SignaturePitchSectionID.CLARITY,
        SignaturePitchSectionID.AUTHORITY,
        SignaturePitchSectionID.PROBLEM,
        SignaturePitchSectionID.SOLUTION,
        SignaturePitchSectionID.THE_WHY,
        SignaturePitchSectionID.OPPORTUNITY,
        SignaturePitchSectionID.NEXT_STEPS,
        SignaturePitchSectionID.ESSENCE,
    ]

    completed_sections = []
    pending_sections = []

    for section in capstone_sections:
        section_state = section_states.get(section.value)
        if section_state and validate_capstone_section_completion(section_state):
            completed_sections.append(section.value)
        else:
            pending_sections.append(section.value)

    return {
        "framework": "CAPSTONE",
        "total_steps": len(capstone_sections),
        "completed_steps": len(completed_sections),
        "remaining_steps": len(pending_sections),
        "completion_percentage": round((len(completed_sections) / len(capstone_sections)) * 100, 1),
        "completed_sections": completed_sections,
        "pending_sections": pending_sections,
        "is_complete": len(pending_sections) == 0,
    }
