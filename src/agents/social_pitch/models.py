"""Pydantic models for Social Pitch Agent."""

import uuid
from enum import Enum
from typing import Any, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field, field_validator


class SectionStatus(str, Enum):
    """Status of a Social Pitch section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SectionID(str, Enum):
    """Social Pitch section identifiers."""
    # The 6 Social Pitch components
    NAME = "name"           # Basic introduction (name, role, company)
    SAME = "same"           # Industry categorization (familiar category)
    FAME = "fame"           # Differentiation (achievements, credentials)
    PAIN = "pain"           # Problem recognition (broad, relatable challenge)
    AIM = "aim"             # Current momentum (90-day focus project)
    GAME = "game"           # Bigger purpose (world change vision)
    
    # Implementation/Export
    IMPLEMENTATION = "implementation"


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


class TiptapNode(BaseModel):
    """Base Tiptap node structure."""
    type: str
    content: list[TiptapInlineNode] | None = Field(None, max_length=5)
    text: str | None = None
    attrs: dict[str, Any] | None = None
    marks: list[dict[str, Any]] | None = Field(None, max_length=2)


class TiptapDocument(BaseModel):
    """Tiptap document structure."""
    type: Literal["doc"] = "doc"
    content: list[TiptapParagraphNode] = Field(default_factory=list, max_length=30)


class SectionContent(BaseModel):
    """Content for a Social Pitch section."""
    content: TiptapDocument  # Rich text content in Tiptap JSON format
    plain_text: str | None = None  # Plain text version for LLM processing


class SectionState(BaseModel):
    """State of a single Social Pitch section."""
    section_id: SectionID
    content: SectionContent | None = None
    score: int | None = Field(None, ge=0, le=5)  # 0-5 rating
    status: SectionStatus = SectionStatus.PENDING


class ContextPacket(BaseModel):
    """Context packet for current section."""
    section_id: SectionID
    status: SectionStatus
    system_prompt: str
    draft: SectionContent | None = None
    validation_rules: dict[str, Any] | None = None


class SocialPitchData(BaseModel):
    """Complete Social Pitch data structure."""
    # Basic information (NAME component)
    user_name: str | None = None
    user_position: str | None = None
    company_name: str | None = None
    
    # SAME component - Industry categorization
    business_category: str | None = None
    target_customer: str | None = None
    same_statement: str | None = None
    
    # FAME component - Differentiation
    fame_tier: str | None = None  # "genuine_fame", "results_awards", "methodology"
    fame_statement: str | None = None
    achievement_details: str | None = None
    
    # PAIN component - Problem recognition
    ideal_clients: str | None = None
    broad_challenge: str | None = None
    pain_statement: str | None = None
    
    # AIM component - Current momentum
    current_project_category: str | None = None  # "raising_investment", "writing_content", etc.
    project_description: str | None = None
    aim_statement: str | None = None
    
    # GAME component - Bigger purpose
    vision_approach: str | None = None  # "world_impact", "mission_vision"
    bigger_vision: str | None = None
    game_statement: str | None = None
    
    # Overall Social Pitch
    complete_pitch: str | None = None
    pitch_confidence: int | None = Field(None, ge=0, le=5)


class ChatAgentOutput(BaseModel):
    """Output from Chat Agent node."""

    reply: str = Field(..., description="Conversational response to the user.")
    router_directive: str = Field(
        ...,
        description="Navigation control: 'stay' to continue on the current section, 'next' to proceed to the next section, or 'modify:<section_id>' to jump to a specific section.",
    )
    is_requesting_rating: bool = Field(
        default=False,
        description="Set to true ONLY when your reply explicitly asks the user for a 0-5 rating."
    )
    score: int | None = Field(
        None, ge=0, le=5, description="Satisfaction score (0-5) if user provided one."
    )
    section_update: dict[str, Any] | None = Field(
        None,
        description="Content for the current section in Tiptap JSON format. REQUIRED when providing summary or asking for rating. Example: {'content': {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'content here'}]}]}}",
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

    @field_validator("section_update")
    def validate_section_update(cls, v):
        """Validate section_update with relaxed rules to allow LLM flexibility."""
        if v is None:
            return v
            
        # Basic structure check - just ensure it's a dict
        if not isinstance(v, dict):
            raise ValueError("Section update must be a dictionary")
            
        # Very minimal validation - just check for obviously broken structure
        if 'content' in v:
            content = v['content']
            if isinstance(content, dict) and 'content' in content:
                # Only check for extremely large content that could cause issues
                if len(content.get('content', [])) > 200:
                    raise ValueError("Section content extremely large - please reduce")
        
        return v


class SocialPitchState(MessagesState):
    """State for Social Pitch agent."""
    # User and document identification
    user_id: int = 1
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Navigation and progress
    current_section: SectionID = SectionID.NAME
    context_packet: ContextPacket | None = None
    section_states: dict[str, SectionState] = Field(default_factory=dict)
    # On initial entry, Router should call get_context directly, so default to NEXT
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    # Social Pitch data
    pitch_data: SocialPitchData = Field(default_factory=SocialPitchData)

    # Memory management
    short_memory: list[BaseMessage] = Field(default_factory=list)

    # Agent output
    agent_output: ChatAgentOutput | None = None
    # Flag indicating the agent has asked a question and is waiting for user's reply
    awaiting_user_input: bool = False
    is_awaiting_rating: bool = False

    # Error tracking
    error_count: int = 0
    last_error: str | None = None


class ValidationRule(BaseModel):
    """Validation rule for field input."""
    field_name: str
    rule_type: Literal["min_length", "max_length", "regex", "required", "choices"]
    value: Any
    error_message: str


class SectionTemplate(BaseModel):
    """Template for a Social Pitch section."""
    section_id: SectionID
    name: str
    description: str
    system_prompt_template: str
    validation_rules: list[ValidationRule] = Field(default_factory=list)
    required_fields: list[str] = Field(default_factory=list)
    next_section: SectionID | None = None


# --- Structured Output Models for Data Extraction ---

class NameData(BaseModel):
    """Structured data for the NAME component."""
    user_name: str | None = Field(None, description="The user's full name.")
    user_position: str | None = Field(None, description="The user's position/role.")
    company_name: str | None = Field(None, description="The company name.")


class SameData(BaseModel):
    """Structured data for the SAME component."""
    business_category: str | None = Field(None, description="The business category (boring and familiar).")
    target_customer: str | None = Field(None, description="The ideal customer group.")
    same_statement: str | None = Field(None, description="The complete SAME statement.")


class FameData(BaseModel):
    """Structured data for the FAME component."""
    fame_tier: str | None = Field(None, description="The tier of fame: genuine_fame, results_awards, or methodology.")
    fame_statement: str | None = Field(None, description="The complete FAME statement.")
    achievement_details: str | None = Field(None, description="Details about the achievement or differentiator.")


class PainData(BaseModel):
    """Structured data for the PAIN component."""
    ideal_clients: str | None = Field(None, description="The ideal client group mentioned in the pain.")
    broad_challenge: str | None = Field(None, description="The broad, relatable challenge.")
    pain_statement: str | None = Field(None, description="The complete PAIN statement.")


class AimData(BaseModel):
    """Structured data for the AIM component."""
    current_project_category: str | None = Field(None, description="The category of current project.")
    project_description: str | None = Field(None, description="Description of the current 90-day focus.")
    aim_statement: str | None = Field(None, description="The complete AIM statement.")


class GameData(BaseModel):
    """Structured data for the GAME component."""
    vision_approach: str | None = Field(None, description="The approach to expressing bigger purpose.")
    bigger_vision: str | None = Field(None, description="The bigger world change vision.")
    game_statement: str | None = Field(None, description="The complete GAME statement.")