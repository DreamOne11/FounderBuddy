'''Pydantic models for Value Canvas Agent.'''

from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field


class SectionStatus(str, Enum):
    """Status of a Value Canvas section."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    MODIFY = "modify"
    GENERATED = "generated"


class RouterDirective(str, Enum):
    """Router directive for navigation control."""
    STAY = "stay"
    NEXT = "next"
    MODIFY = "modify"  # Format: "modify:section_id"


class SectionID(str, Enum):
    """Value Canvas section identifiers."""
    # Initial Interview
    INTERVIEW = "interview"

    # Core Value Canvas Sections (7 total according to document)
    ICP = "icp"  # Ideal Customer Persona
    PAIN = "pain"  # The Pain (contains 3 pain points)
    DEEP_FEAR = "deep_fear"  # The Deep Fear
    PAYOFFS = "payoffs"  # The Payoffs (contains 3 payoff points)
    SIGNATURE_METHOD = "signature_method"  # Signature Method
    MISTAKES = "mistakes"  # The Mistakes
    PRIZE = "prize"  # The Prize

    # Implementation/Export
    IMPLEMENTATION = "implementation"


class TiptapNode(BaseModel):
    """Base Tiptap node structure."""
    type: str
    content: Optional[List[Dict[str, Any]]] = None
    text: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None
    marks: Optional[List[Dict[str, Any]]] = None


class TiptapDocument(BaseModel):
    """Tiptap document structure."""
    type: Literal["doc"] = "doc"
    content: List[TiptapNode] = Field(default_factory=list)


class SectionContent(BaseModel):
    """Content for a Value Canvas section."""
    content: TiptapDocument  # Rich text content in Tiptap JSON format
    plain_text: Optional[str] = None  # Plain text version for LLM processing


class SectionState(BaseModel):
    """State of a single Value Canvas section."""
    id: UUID
    user_id: UUID
    doc_id: UUID
    section_id: SectionID
    content: Optional[SectionContent] = None
    score: Optional[int] = Field(None, ge=0, le=5)  # 0-5 rating
    status: SectionStatus = SectionStatus.PENDING
    updated_at: Optional[str] = None  # ISO timestamp


class ContextPacket(BaseModel):
    """Context packet for current section."""
    section_id: SectionID
    status: SectionStatus
    system_prompt: str
    draft: Optional[SectionContent] = None
    section_template: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None


class ValueCanvasData(BaseModel):
    """Complete Value Canvas data structure."""
    # Basic information from initial interview
    client_name: Optional[str] = None
    preferred_name: Optional[str] = None  # 添加昵称字段
    company_name: Optional[str] = None
    industry: Optional[str] = None
    standardized_industry: Optional[str] = None
    specialty: Optional[str] = None
    career_highlight: Optional[str] = None
    client_outcomes: Optional[str] = None
    awards_media: Optional[str] = None
    published_content: Optional[str] = None
    published_content_types: Optional[str] = None  # 添加发布内容类型字段
    specialized_skills: Optional[str] = None
    notable_partners: Optional[str] = None

    # ICP data
    icp_standardized_role: Optional[str] = None
    icp_demographics: Optional[str] = None
    icp_geography: Optional[str] = None
    icp_nickname: Optional[str] = None
    icp_affinity: Optional[str] = None
    icp_affordability: Optional[str] = None
    icp_impact: Optional[str] = None
    icp_access: Optional[str] = None

    # Pain points (3)
    pain1_symptom: Optional[str] = None
    pain1_struggle: Optional[str] = None
    pain1_cost: Optional[str] = None
    pain1_consequence: Optional[str] = None

    pain2_symptom: Optional[str] = None
    pain2_struggle: Optional[str] = None
    pain2_cost: Optional[str] = None
    pain2_consequence: Optional[str] = None

    pain3_symptom: Optional[str] = None
    pain3_struggle: Optional[str] = None
    pain3_cost: Optional[str] = None
    pain3_consequence: Optional[str] = None

    # Deep Fear
    deep_fear: Optional[str] = None

    # Payoffs (3)
    payoff1_objective: Optional[str] = None
    payoff1_desire: Optional[str] = None
    payoff1_without: Optional[str] = None
    payoff1_resolution: Optional[str] = None

    payoff2_objective: Optional[str] = None
    payoff2_desire: Optional[str] = None
    payoff2_without: Optional[str] = None
    payoff2_resolution: Optional[str] = None

    payoff3_objective: Optional[str] = None
    payoff3_desire: Optional[str] = None
    payoff3_without: Optional[str] = None
    payoff3_resolution: Optional[str] = None

    # Signature Method
    method_name: Optional[str] = None
    sequenced_principles: Optional[List[str]] = None
    principle_descriptions: Optional[Dict[str, str]] = None

    # Mistakes
    mistakes: Optional[List[Dict[str, Any]]] = None

    # Prize
    prize_category: Optional[str] = None
    prize_statement: Optional[str] = None
    refined_prize: Optional[str] = None


class ChatAgentOutput(BaseModel):
    """Output from Chat Agent node."""
    reply: str  # Response to user
    router_directive: str  # Navigation control
    score: Optional[int] = Field(None, ge=0, le=5)  # Section score
    section_update: Optional[SectionContent] = None  # Content update


class ValueCanvasState(MessagesState):
    """State for Value Canvas agent."""
    # User and document identification
    user_id: str = "studio-user"
    doc_id: str = "studio-doc"

    # Navigation and progress
    current_section: SectionID = SectionID.INTERVIEW
    context_packet: Optional[ContextPacket] = None
    section_states: Dict[str, SectionState] = Field(default_factory=dict)
    # 初次进入希望 Router 直接调用 get_context，所以默认 NEXT
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    # Value Canvas data
    canvas_data: ValueCanvasData = Field(default_factory=ValueCanvasData)

    # Memory management
    short_memory: List[BaseMessage] = Field(default_factory=list)

    # Agent output
    agent_output: Optional[ChatAgentOutput] = None
    # Flag indicating the agent has asked a question and is waiting for user's reply
    awaiting_user_input: bool = False

    # Error tracking
    error_count: int = 0
    last_error: Optional[str] = None


class ValidationRule(BaseModel):
    """Validation rule for field input."""
    field_name: str
    rule_type: Literal["min_length", "max_length", "regex", "required", "choices"]
    value: Any
    error_message: str


class SectionTemplate(BaseModel):
    """Template for a Value Canvas section."""
    section_id: SectionID
    name: str
    description: str
    system_prompt_template: str
    validation_rules: List[ValidationRule] = Field(default_factory=list)
    required_fields: List[str] = Field(default_factory=list)
    next_section: Optional[SectionID] = None


# --- Structured Output Models for Data Extraction ---

class InterviewData(BaseModel):
    """A data structure to hold extracted information from the user interview."""
    
    client_name: Optional[str] = Field(
        None, 
        description="The user's full name. Exclude any mention of a preferred name."
    )
    preferred_name: Optional[str] = Field(
        None, 
        description="The user's preferred name or nickname, often found in parentheses."
    )
    company_name: Optional[str] = Field(
        None, 
        description="The name of the user's company."
    )
    industry: Optional[str] = Field(
        None, 
        description="The industry the user works in."
    )
    specialty: Optional[str] = Field(
        None, 
        description="The user's specialty or 'zone of genius'."
    )
    career_highlight: Optional[str] = Field(
        None, 
        description="A career achievement the user is proud of."
    )
    client_outcomes: Optional[str] = Field(
        None, 
        description="The typical results or outcomes clients get from working with the user."
    )
    specialized_skills: Optional[str] = Field(
        None, 
        description="Specific skills or qualifications the user mentioned."
    )


class ICPData(BaseModel):
    """Structured data for the Ideal Client Persona (ICP) section."""
    nickname: Optional[str] = Field(None, description="A short, memorable nickname for the ICP.")
    role_and_sector: Optional[str] = Field(None, description="The ICP's professional role and the sector they operate in.")
    demographics: Optional[str] = Field(None, description="Key demographic information about the ICP (e.g., age, income, family status).")
    geography: Optional[str] = Field(None, description="The geographic location where the ICP is typically found.")
    affinity: Optional[str] = Field(None, description="Assessment of whether you would enjoy working with this ICP.")
    affordability: Optional[str] = Field(None, description="Assessment of the ICP's ability to afford premium pricing.")
    impact: Optional[str] = Field(None, description="Assessment of the potential significance of your solution's impact on the ICP.")
    access: Optional[str] = Field(None, description="Assessment of how easily you can reach and connect with this ICP.")


class PainPoint(BaseModel):
    """Structured data for a single pain point."""
    symptom: Optional[str] = Field(None, description="The observable problem or symptom of the pain (1-3 words).")
    struggle: Optional[str] = Field(None, description="How this pain shows up in their daily work life (1-2 sentences).")
    cost: Optional[str] = Field(None, description="The immediate, tangible cost of this pain.")
    consequence: Optional[str] = Field(None, description="The long-term, future consequence if this pain is not solved.")


class PainData(BaseModel):
    """Structured data for the Pain section, containing three distinct pain points."""
    pain_points: List[PainPoint] = Field(description="A list of three distinct pain points.")


class DeepFearData(BaseModel):
    """Structured data for the Deep Fear section."""
    deep_fear: Optional[str] = Field(None, description="The private doubt or self-question the client has that they rarely voice.")


class PayoffPoint(BaseModel):
    """Structured data for a single payoff point."""
    objective: Optional[str] = Field(None, description="What the client wants to achieve (1-3 words).")
    desire: Optional[str] = Field(None, description="A description of what the client specifically wants (1-2 sentences).")
    without: Optional[str] = Field(None, description="A statement that pre-handles common objections or concerns.")
    resolution: Optional[str] = Field(None, description="A statement that directly resolves the corresponding pain symptom.")


class PayoffsData(BaseModel):
    """Structured data for the Payoffs section, containing three distinct payoff points."""
    payoffs: List[PayoffPoint] = Field(description="A list of three distinct payoff points that mirror the pain points.")


class Principle(BaseModel):
    """A single principle within the Signature Method."""
    name: Optional[str] = Field(None, description="The name of the principle (2-4 words).")
    description: Optional[str] = Field(None, description="A brief description of what the principle means in practice (1-2 sentences).")


class SignatureMethodData(BaseModel):
    """Structured data for the Signature Method section."""
    method_name: Optional[str] = Field(None, description="A memorable name for the method (2-4 words).")
    principles: List[Principle] = Field(description="A list of 4-6 core principles that form the method.")


class Mistake(BaseModel):
    """Structured data for a single mistake."""
    related_to: str = Field(description="The pain point or method principle this mistake is related to.")
    root_cause: Optional[str] = Field(None, description="The non-obvious reason this mistake keeps happening.")
    error_in_thinking: Optional[str] = Field(None, description="The flawed belief that makes the problem worse.")
    error_in_action: Optional[str] = Field(None, description="What they do that feels right but creates more problems.")


class MistakesData(BaseModel):
    """Structured data for the Mistakes section."""
    mistakes: List[Mistake] = Field(description="A list of mistakes related to pain points and method principles.")


class PrizeData(BaseModel):
    """Structured data for the Prize section."""
    category: Optional[str] = Field(None, description="The category of the prize (e.g., Identity-Based, Outcome-Based).")
    statement: Optional[str] = Field(None, description="The 1-5 word prize statement.") 