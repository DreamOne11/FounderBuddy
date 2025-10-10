"""Pydantic models for Concept Pitch Agent."""

import uuid
from typing import Any, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field, field_validator

# Import enums and base models
from .enums import RouterDirective, SectionID, SectionStatus
from .sections.base_prompt import SectionTemplate, ValidationRule


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


class TiptapListItemNode(BaseModel):
    """Tiptap list item node."""
    type: Literal["listItem"] = "listItem"
    content: list['TiptapParagraphNode'] = Field(default_factory=list, max_length=10)
    attrs: dict[str, Any] | None = None


class TiptapBulletListNode(BaseModel):
    """Tiptap bullet list node."""
    type: Literal["bulletList"] = "bulletList"
    content: list[TiptapListItemNode] = Field(default_factory=list, max_length=20)
    attrs: dict[str, Any] | None = None


class TiptapOrderedListNode(BaseModel):
    """Tiptap ordered list node."""
    type: Literal["orderedList"] = "orderedList"
    content: list[TiptapListItemNode] = Field(default_factory=list, max_length=20)
    attrs: dict[str, Any] | None = None


class TiptapHeadingNode(BaseModel):
    """Tiptap heading node."""
    type: Literal["heading"] = "heading"
    attrs: dict[str, int] = Field(default={"level": 2})  # Default to h2
    content: list[TiptapInlineNode] = Field(default_factory=list, max_length=10)


class TiptapNode(BaseModel):
    """Base Tiptap node structure."""
    type: str
    content: list[TiptapInlineNode] | None = Field(None, max_length=5)
    text: str | None = None
    attrs: dict[str, Any] | None = None
    marks: list[dict[str, Any]] | None = Field(None, max_length=2)


# Union type for block content nodes (paragraphs, lists, and headings)
TiptapBlockNode = TiptapParagraphNode | TiptapBulletListNode | TiptapOrderedListNode | TiptapHeadingNode


class TiptapDocument(BaseModel):
    """Tiptap document structure."""
    type: Literal["doc"] = "doc"
    content: list[TiptapBlockNode] = Field(default_factory=list, max_length=30)


class SectionContent(BaseModel):
    """Content for a Concept Pitch section."""
    content: TiptapDocument  # Rich text content in Tiptap JSON format
    plain_text: str | None = None  # Plain text version for LLM processing


class SectionState(BaseModel):
    """State of a single Concept Pitch section."""
    section_id: SectionID
    content: SectionContent | None = None
    satisfaction_status: str | None = None  # satisfied, needs_improvement, or None
    status: SectionStatus = SectionStatus.PENDING


class ContextPacket(BaseModel):
    """Context packet for current section."""
    section_id: SectionID
    status: SectionStatus
    system_prompt: str
    draft: SectionContent | None = None
    validation_rules: dict[str, Any] | None = None


class ConceptPitchData(BaseModel):
    """Complete Concept Pitch data structure."""
    # RAG data from Value Canvas
    icp_summary: str | None = None
    pain_summary: str | None = None
    gain_summary: str | None = None
    prize_summary: str | None = None
    
    # Generated pitches
    pain_driven_pitch: str | None = None
    gain_driven_pitch: str | None = None
    prize_driven_pitch: str | None = None
    
    # Selected and refined pitch
    selected_pitch_type: str | None = None  # "pain", "gain", "prize"
    final_pitch: str | None = None
    
    # User feedback
    user_satisfaction: bool | None = None
    refinement_notes: str | None = None


class ChatAgentDecision(BaseModel):
    """Structured decision data from Decision Agent node."""
    
    router_directive: str = Field(
        ...,
        description="Navigation control: 'stay' to continue on the current section, 'next' to proceed to the next section, or 'modify:<section_id>' to jump to a specific section.",
    )
    user_satisfaction_feedback: str | None = Field(
        None, description="User's natural language feedback about satisfaction with the section content."
    )
    is_satisfied: bool | None = Field(
        None, description="AI's interpretation of user satisfaction based on their feedback. True if satisfied, False if needs improvement."
    )
    should_save_content: bool = Field(
        False,
        description="Whether the AI just presented a summary that should be saved. True when presenting section summary for user review, False when still collecting information.",
    )

    @field_validator("router_directive")
    def validate_router_directive(cls, v):
        """Validate the router_directive field."""
        if v not in ["stay", "next"] and not v.startswith("modify:"):
            raise ValueError(
                "router_directive must be 'stay', 'next', or start with 'modify:'"
            )
        if v.startswith("modify:"):
            section_id = v.split(":", 1)[1]
            if not section_id:
                raise ValueError("modify directive must include a section_id")
        return v


class ChatAgentOutput(BaseModel):
    """Complete output from Chat Agent (reply + decision data)."""

    reply: str = Field(..., description="Conversational response to the user.")
    router_directive: str = Field(
        ...,
        description="Navigation control: 'stay' to continue on the current section, 'next' to proceed to the next section, or 'modify:<section_id>' to jump to a specific section.",
    )
    user_satisfaction_feedback: str | None = Field(
        None, description="User's natural language feedback about satisfaction with the section content."
    )
    is_satisfied: bool | None = Field(
        None, description="AI's interpretation of user satisfaction based on their feedback. True if satisfied, False if needs improvement."
    )
    section_update: dict[str, Any] | None = Field(
        None,
        description="[DEPRECATED - Will be removed] Section data is now extracted by memory_updater, not generated by decision node.",
    )
    should_save_content: bool = Field(
        False,
        description="Whether the AI just presented a summary that should be saved. True when presenting section summary for user review, False when still collecting information.",
    )

    @field_validator("router_directive")
    def validate_router_directive(cls, v):
        """Validate the router_directive field."""
        if v not in ["stay", "next"] and not v.startswith("modify:"):
            raise ValueError(
                "router_directive must be 'stay', 'next', or start with 'modify:'"
            )
        if v.startswith("modify:"):
            section_id = v.split(":", 1)[1]
            if not section_id:
                raise ValueError("modify directive must include a section_id")
        return v


class ConceptPitchState(MessagesState):
    """State for Concept Pitch agent."""
    # User and document identification
    user_id: int = 1
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Navigation and progress
    current_section: SectionID = SectionID.SUMMARY_CONFIRMATION
    context_packet: ContextPacket | None = None
    section_states: dict[str, SectionState] = Field(default_factory=dict)
    # On initial entry, Router should call get_context directly, so default to NEXT
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    # Concept Pitch data
    canvas_data: ConceptPitchData = Field(default_factory=ConceptPitchData)

    # Memory management
    short_memory: list[BaseMessage] = Field(default_factory=list)

    # Agent output
    agent_output: ChatAgentOutput | None = None
    # Flag indicating the agent has asked a question and is waiting for user's reply
    awaiting_user_input: bool = False
    awaiting_satisfaction_feedback: bool = False  # Track if we're waiting for user satisfaction feedback

    # Error tracking
    error_count: int = 0
    last_error: str | None = None


# Export all models for backward compatibility
__all__ = [
    # Core enums and classes
    "SectionStatus",
    "RouterDirective",
    "SectionID",
    # Tiptap models
    "TiptapTextNode",
    "TiptapHardBreakNode",
    "TiptapInlineNode",
    "TiptapParagraphNode",
    "TiptapNode",
    "TiptapDocument",
    # Section models
    "SectionContent",
    "SectionState",
    "ContextPacket",
    "ConceptPitchData",
    "ChatAgentDecision",
    "ChatAgentOutput",
    "ConceptPitchState",
    "ValidationRule",
    "SectionTemplate",
]
