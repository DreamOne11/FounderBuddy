"""Pydantic models for Special Report Agent."""

import uuid
from typing import Any, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field, field_validator

from .enums import RouterDirective, SectionStatus, SpecialReportSection
from .framework_models import SpecialReportCanvasData, FrameworkSectionState


class TiptapTextNode(BaseModel):
    """Tiptap text node."""

    type: Literal["text"] = "text"
    text: str
    marks: list[dict[str, Any]] | None = Field(None, max_length=5)


class TiptapHardBreakNode(BaseModel):
    """Tiptap hard break node."""

    type: Literal["hardBreak"] = "hardBreak"


# Union type for inline content nodes
TiptapInlineNode = TiptapTextNode | TiptapHardBreakNode


class TiptapParagraphNode(BaseModel):
    """Tiptap paragraph node."""

    type: Literal["paragraph"] = "paragraph"
    content: list[TiptapInlineNode] = Field(default_factory=list, max_length=50)
    attrs: dict[str, Any] | None = None


class TiptapDocument(BaseModel):
    """Tiptap document structure."""

    type: Literal["doc"] = "doc"
    content: list[TiptapParagraphNode] = Field(default_factory=list, max_length=30)


class SectionContent(BaseModel):
    """Content for a section."""

    content: TiptapDocument  # Rich text content in Tiptap JSON format
    plain_text: str | None = None  # Plain text version for LLM processing


class SectionState(BaseModel):
    """State of a single section."""

    section_id: SpecialReportSection
    content: SectionContent | None = None
    satisfaction_feedback: str | None = None  # User's satisfaction feedback
    status: SectionStatus = SectionStatus.PENDING


class ContextPacket(BaseModel):
    """Context packet for current section."""

    section_id: SpecialReportSection
    status: SectionStatus
    system_prompt: str
    draft: SectionContent | None = None
    validation_rules: dict[str, Any] | None = None


# Legacy data models removed - using framework_models.py instead


class ChatAgentOutput(BaseModel):
    """Output from Chat Agent node."""

    reply: str = Field(..., description="Conversational response to the user.")
    router_directive: str = Field(
        ...,
        description="Navigation control: 'stay' to continue on the current section, 'next' to proceed to the next section, or 'modify:<section_id>' to jump to a specific section.",
    )
    is_requesting_rating: bool = Field(
        default=False,
        description="Set to true ONLY when your reply explicitly asks the user for a satisfaction rating.",
    )
    user_satisfaction_feedback: str | None = Field(
        None,
        description="User's natural language feedback about satisfaction with the section content.",
    )
    is_satisfied: bool | None = Field(
        None,
        description="AI's interpretation of user satisfaction based on their feedback. True if satisfied, False if needs improvement.",
    )
    section_update: dict[str, Any] | None = Field(
        None,
        description="Content for the current section in Tiptap JSON format. REQUIRED when providing summary or asking for rating. Example: {'content': {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'content here'}]}]}}",
    )

    @field_validator("router_directive")
    def validate_router_directive(cls, v):
        """Validate the router_directive field."""
        if v not in ["stay", "next"] and not v.startswith("modify:"):
            raise ValueError("router_directive must be 'stay', 'next', or start with 'modify:'")
        if v.startswith("modify:"):
            section_id = v.split(":", 1)[1]
            if not section_id:
                raise ValueError("modify directive must include a section_id")
        return v

    @field_validator("section_update")
    def validate_section_update(cls, v):
        """Validate section_update with relaxed rules to allow LLM flexibility."""
        if v is None:
            return v

        # Basic structure check - just ensure it's a dict
        if not isinstance(v, dict):
            raise ValueError("Section update must be a dictionary")

        # Very minimal validation - just check for obviously broken structure
        if "content" in v:
            content = v["content"]
            if isinstance(content, dict) and "content" in content:
                # Only check for extremely large content that could cause issues
                if len(content.get("content", [])) > 200:  # Much more lenient limit
                    raise ValueError("Section content extremely large - please reduce")

        return v


class SpecialReportState(MessagesState):
    """State for Special Report agent."""

    # User and document identification
    user_id: int = 1
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Navigation and progress
    current_section: SpecialReportSection = SpecialReportSection.ATTRACT
    context_packet: ContextPacket | None = None
    section_states: dict[str, SectionState] = Field(default_factory=dict)
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    # Special Report data - using framework structure
    canvas_data: SpecialReportCanvasData = Field(default_factory=SpecialReportCanvasData)

    # Memory management
    short_memory: list[BaseMessage] = Field(default_factory=list)

    # Agent output
    agent_output: ChatAgentOutput | None = None
    awaiting_user_input: bool = False
    is_awaiting_rating: bool = False

    # Error tracking
    error_count: int = 0
    last_error: str | None = None

    # Safety mechanism for stuck states
    consecutive_stays: int = 0


class ValidationRule(BaseModel):
    """Validation rule for field input."""

    field_name: str
    rule_type: Literal["min_length", "max_length", "regex", "required", "choices"]
    value: Any
    error_message: str


class SectionTemplate(BaseModel):
    """Template for a section."""

    section_id: SpecialReportSection
    name: str
    description: str
    system_prompt_template: str
    validation_rules: list[ValidationRule] = Field(default_factory=list)
    required_fields: list[str] = Field(default_factory=list)
    next_section: SpecialReportSection | None = None
