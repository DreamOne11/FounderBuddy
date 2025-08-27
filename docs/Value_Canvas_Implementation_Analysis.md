# Value Canvas Agent - Complete Implementation Analysis

## Overview

This document provides a detailed breakdown of how the Value Canvas Agent is implemented, serving as the definitive reference for understanding the architecture, patterns, and implementation details. Use this as the template for implementing other agents.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [File Structure Analysis](#file-structure-analysis)
3. [Prompts Deep Dive](#prompts-deep-dive)
4. [Data Models Architecture](#data-models-architecture)
5. [LangGraph Flow Implementation](#langgraph-flow-implementation)
6. [Tools & External Integration](#tools--external-integration)
7. [Key Implementation Patterns](#key-implementation-patterns)
8. [Critical Success Factors](#critical-success-factors)

---

## Architecture Overview

### The LangGraph Pattern
```
Start → Initialize → Router → Chat Agent → Memory Updater → Router
                       ↓                                    ↑
                  Implementation ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘
```

### Core Nodes Responsibilities:

1. **Initialize Node**: Sets up state with user/thread IDs, ensures all required fields exist
2. **Router Node**: Handles navigation (stay/next/modify), loads section context, manages transitions
3. **Chat Agent Node**: Domain-specific conversations, generates responses, validates input
4. **Memory Updater Node**: Persists data, updates canvas state, manages section completion
5. **Implementation Node**: Generates final deliverables when all sections complete

---

## File Structure Analysis

### **src/agents/value_canvas/**

```
value_canvas/
├── __init__.py          # Package exports (graph, initialize_function)
├── agent.py             # LangGraph StateGraph implementation (1,107 lines)
├── models.py            # Pydantic models and state management (396 lines)
├── prompts.py           # Section prompts and templates (1,438 lines)
├── tools.py             # External integrations and utilities (735 lines)
└── docs/                # Documentation and reference materials
```

**Key Insight**: The **prompts.py** file is the largest (1,438 lines) because it contains the domain expertise and conversation flows that make the agent unique.

---

## Prompts Deep Dive

### **Base Rules (Universal System Prompt)**
The foundation prompt that applies to ALL sections:

```python
SECTION_PROMPTS = {
    "base_rules": """You are a street-smart marketing expert who helps business owners create Value Canvas frameworks...

COMMUNICATION STYLE:
- Use direct, plain language that business owners understand immediately
- Avoid corporate buzzwords, consultant speak, and MBA terminology  
- Base responses on facts and first principles, not hype or excessive adjectives
- Be concise - use words sparingly and purposefully
- Never praise, congratulate, or pander to users

LANGUAGE EXAMPLES:
❌ Avoid: "Industry leaders exhibit proactivity in opportunity acquisition through strategic visibility"
✅ Use: "Key people don't chase opportunities, they curate them"

OUTPUT PHILOSOPHY:
- Create working first drafts that users can test in the market
- Never present output as complete or final - everything is directional
- Always seek user feedback: "Which would resonate most with your ICP?" or "Which would you be comfortable saying to a prospect?"
- Provide multiple options when possible
- Remember: You can't tell them what will work, only get them directionally correct

CRITICAL OUTPUT REQUIREMENTS:
You MUST ALWAYS output your response in the following JSON format. Your entire response should be valid JSON:

{
  "reply": "Your conversational response to the user",
  "router_directive": "stay|next|modify:section_id", 
  "score": null,
  "section_update": null
}"""
}
```

**Key Patterns:**
1. **Domain Expert Persona**: "Street-smart marketing expert" 
2. **Communication Rules**: Direct language, avoid jargon
3. **Output Format**: Structured JSON with specific fields
4. **Philosophy**: Working drafts, market testing, user feedback

### **Section-Specific Templates**
Each section has detailed prompts with specific conversation flows:

#### **Interview Section** (Example)
```python
SectionID.INTERVIEW.value: SectionTemplate(
    name="Initial Interview",
    description="Collect basic information about the client and their business",
    system_prompt_template="""
    INTERVIEW SECTION FLOW:
    This section follows a STRICT 7-step conversation flow:
    
    STEP 1 - Welcome:
    "Let's build your Value Canvas! Are you ready to get started?"
    
    STEP 2 - Context about AI:
    "Firstly, some context on working with me as an AI..."
    
    STEP 3 - Context about Value Canvas:
    "Great! Now, some context around the Value Canvas itself..."
    
    [... detailed step-by-step flow ...]
    """,
    validation_rules=[...],
    required_fields=["client_name", "preferred_name", "company_name", "industry"],
)
```

#### **ICP Section** (Advanced Example)
```python
SectionID.ICP.value: SectionTemplate(
    name="Ideal Client Persona",
    description="Define the ultimate decision-maker who will be the focus of the Value Canvas",
    system_prompt_template="""
    CRITICAL INSTRUCTION FOR YOUR FIRST MESSAGE:
    When you start this section, your very first message should include:
    "Let me start with some context around your ICP..."
    
    ABSOLUTE RULES FOR THIS SECTION:
    1. You are FORBIDDEN from asking multiple questions at once. EXACTLY ONE question. 
    2. You MUST collect ALL 8 required fields before showing any ICP summary
    3. NEVER use router_directive "next" until: all 8 fields + complete ICP output + user rating ≥ 3
    
    ICP TEMPLATE - THE 8 SECTIONS YOU MUST COLLECT:
    1. ICP NICKNAME: You will create a compelling 2-4 word nickname
    2. ROLE/IDENTITY: Their primary role or life situation
    3. CONTEXT/SCALE: Company size, team size, funding, etc.
    4. INDUSTRY/SECTOR CONTEXT: Industry + key insight about sector
    5. DEMOGRAPHICS: Gender, age range, income/budget, location
    6. INTERESTS: 3 specific interests (primary, secondary, tertiary)
    7. VALUES: 2 lifestyle indicators that show their values
    8. GOLDEN INSIGHT: A profound insight about their buying motivations
    """,
)
```

**Key Implementation Patterns:**
1. **Structured Flows**: Step-by-step conversation sequences
2. **Validation Rules**: Required fields and completion criteria  
3. **Output Templates**: Specific format for section summaries
4. **Conversation Control**: One question at a time, validation before proceeding

---

## Data Models Architecture

### **Core State Model**
```python
class ValueCanvasState(MessagesState):
    """State for Value Canvas agent."""
    # User and document identification
    user_id: int = 1
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Navigation and progress
    current_section: SectionID = SectionID.INTERVIEW
    context_packet: ContextPacket | None = None
    section_states: dict[str, SectionState] = Field(default_factory=dict)
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    # Value Canvas data
    canvas_data: ValueCanvasData = Field(default_factory=ValueCanvasData)

    # Memory management
    short_memory: list[BaseMessage] = Field(default_factory=list)

    # Agent output
    agent_output: ChatAgentOutput | None = None
    awaiting_user_input: bool = False
    is_awaiting_rating: bool = False

    # Error tracking
    error_count: int = 0
    last_error: str | None = None
```

### **Section Identifiers**
```python
class SectionID(str, Enum):
    """Value Canvas section identifiers."""
    INTERVIEW = "interview"
    ICP = "icp"  # Ideal Customer Persona
    PAIN = "pain"  # The Pain (contains 3 pain points)
    DEEP_FEAR = "deep_fear"  # The Deep Fear
    PAYOFFS = "payoffs"  # The Payoffs (contains 3 payoff points)
    SIGNATURE_METHOD = "signature_method"  # Signature Method
    MISTAKES = "mistakes"  # The Mistakes
    PRIZE = "prize"  # The Prize
    IMPLEMENTATION = "implementation"
```

### **Canvas Data Structure**
```python
class ValueCanvasData(BaseModel):
    """Complete Value Canvas data structure."""
    # Basic information from initial interview
    client_name: str | None = None
    preferred_name: str | None = None
    company_name: str | None = None
    industry: str | None = None
    # ... other interview fields

    # ICP data - corresponds to the 8 sections in ICP Template
    icp_nickname: str | None = None
    icp_role_identity: str | None = None
    icp_context_scale: str | None = None
    # ... other ICP fields

    # Pain points (3 complete pain points)
    pain1_symptom: str | None = None
    pain1_struggle: str | None = None
    pain1_cost: str | None = None
    pain1_consequence: str | None = None
    # ... pain2, pain3

    # All other sections follow similar detailed field structure
```

### **Chat Agent Output**
```python
class ChatAgentOutput(BaseModel):
    """Output from Chat Agent node."""
    reply: str = Field(..., description="Conversational response to the user.")
    router_directive: str = Field(..., description="Navigation control: 'stay'/'next'/'modify:<section_id>'")
    is_requesting_rating: bool = Field(default=False, description="Set to true ONLY when explicitly asking for 0-5 rating")
    score: int | None = Field(None, ge=0, le=5, description="Satisfaction score if user provided one")
    section_update: dict[str, Any] | None = Field(None, description="Tiptap JSON content when showing summary")
```

**Key Patterns:**
1. **Hierarchical State**: Global state → Section states → Individual field data
2. **Rich Data Models**: Every section has detailed field breakdown
3. **Validation**: Pydantic models with field validators
4. **TipTap Integration**: Rich text content in structured JSON format

---

## LangGraph Flow Implementation

### **Initialize Node**
```python
async def initialize_node(state: ValueCanvasState, config: RunnableConfig) -> ValueCanvasState:
    """Initialize node that ensures all required state fields are present."""
    # Get correct IDs from config
    configurable = config.get("configurable", {})
    
    if "user_id" not in state or not state["user_id"]:
        if "user_id" in configurable and configurable["user_id"]:
            state["user_id"] = configurable["user_id"]
        else:
            raise ValueError("Critical system error: No valid user_id found")
    
    # Ensure all required fields have default values
    if "current_section" not in state:
        state["current_section"] = SectionID.INTERVIEW
    if "router_directive" not in state:
        state["router_directive"] = RouterDirective.NEXT
    # ... other field initializations
    
    return state
```

### **Router Node**
```python
async def router_node(state: ValueCanvasState, config: RunnableConfig) -> ValueCanvasState:
    """Router node that handles navigation and context loading."""
    directive = state.get("router_directive", RouterDirective.STAY)
    
    if directive == RouterDirective.STAY:
        # Stay on current section, no context reload needed
        return state
    
    elif directive == RouterDirective.NEXT:
        # Find next unfinished section
        next_section = get_next_unfinished_section(state.get("section_states", {}))
        if next_section:
            state["current_section"] = next_section
            # Get context for new section
            context = await get_context.ainvoke({
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "section_id": next_section.value,
                "canvas_data": state["canvas_data"].model_dump(),
            })
            state["context_packet"] = ContextPacket(**context)
            state["router_directive"] = RouterDirective.STAY
        else:
            state["finished"] = True
    
    elif directive.startswith("modify:"):
        # Jump to specific section
        section_id = directive.split(":", 1)[1]
        new_section = SectionID(section_id)
        state["current_section"] = new_section
        # Get context for new section
        # ... similar to NEXT logic
    
    return state
```

### **Chat Agent Node**
```python
async def chat_agent_node(state: ValueCanvasState, config: RunnableConfig) -> ValueCanvasState:
    """Chat agent node that handles section-specific conversations."""
    # Get LLM with structured output
    llm = get_model()
    structured_llm = llm.with_structured_output(ChatAgentOutput, method="function_calling")
    
    # Build message context
    messages: list[BaseMessage] = []
    
    # Add system prompt from context packet
    if state.get("context_packet"):
        messages.append(SystemMessage(content=state["context_packet"].system_prompt))
    
    # Add conversation history
    messages.extend(state.get("short_memory", []))
    
    # Add last human message
    if state.get("messages"):
        last_msg = state["messages"][-1]
        if isinstance(last_msg, HumanMessage):
            messages.append(last_msg)
    
    # Get structured output from LLM
    llm_output = await structured_llm.ainvoke(messages)
    
    # Process output and update state
    state["agent_output"] = llm_output
    state["router_directive"] = llm_output.router_directive
    state["messages"].append(AIMessage(content=llm_output.reply))
    
    return state
```

### **Memory Updater Node**
```python
async def memory_updater_node(state: ValueCanvasState, config: RunnableConfig) -> ValueCanvasState:
    """Memory updater node that persists section states and updates canvas data."""
    agent_out = state.get("agent_output")
    
    if agent_out and agent_out.section_update:
        section_id = state["current_section"].value
        
        # Save to database
        await save_section.ainvoke({
            "user_id": state["user_id"],
            "thread_id": state["thread_id"],
            "section_id": section_id,
            "content": agent_out.section_update['content'],
            "score": agent_out.score,
            "status": computed_status,
        })
        
        # Update local state
        state["section_states"][section_id] = SectionState(
            section_id=SectionID(section_id),
            content=SectionContent(content=tiptap_doc),
            score=agent_out.score,
            status=computed_status,
        )
        
        # Extract structured data and update canvas_data
        # Uses LLM to extract specific fields from content
        
    return state
```

**Key Patterns:**
1. **Async/Await**: All nodes are async for database operations
2. **State Validation**: Each node validates and ensures state consistency
3. **Error Handling**: Comprehensive error handling and logging
4. **Tool Integration**: Nodes use tools for external operations

---

## Tools & External Integration

### **Core Tools**
```python
# Router tools
router_tools = [get_context]

# Memory updater tools  
memory_updater_tools = [
    save_section,
    get_all_sections_status, 
    create_tiptap_content,
    extract_plain_text,
    validate_field,
]

# Implementation tools
implementation_tools = [export_checklist]
```

### **Key Tool Examples**

#### **get_context Tool**
```python
@tool
async def get_context(
    user_id: int,
    thread_id: str, 
    section_id: str,
    canvas_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Get context packet for a specific Value Canvas section."""
    # Get section template
    template = SECTION_TEMPLATES.get(section_id)
    
    # Generate system prompt with template rendering
    base_prompt = SECTION_PROMPTS.get("base_rules", "")
    section_prompt = template.system_prompt_template
    
    # Safe partial template rendering
    if canvas_data:
        section_prompt = re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", 
                               lambda m: str(canvas_data.get(m.group(1), "")), 
                               section_prompt)
    
    system_prompt = f"{base_prompt}\\n\\n---\\n\\n{section_prompt}"
    
    # Fetch existing draft from database
    # ... database integration logic
    
    return {
        "system_prompt": system_prompt,
        "draft": draft,
        "status": status,
        "validation_rules": template.validation_rules,
    }
```

#### **save_section Tool**
```python
@tool
async def save_section(
    user_id: int,
    thread_id: str,
    section_id: str,
    content: dict[str, Any],
) -> dict[str, Any]:
    """Save section content to database."""
    # Database integration with DentApp API
    if settings.USE_DENTAPP_API:
        section_id_int = get_section_id_int(section_id)
        # ... API call to save data
    
    return {
        "success": True,
        "section_id": section_id,
        "timestamp": datetime.now().isoformat(),
    }
```

**Integration Points:**
1. **DentApp API**: External database for persistence
2. **TipTap Format**: Rich text content management
3. **Section ID Mapping**: Maps section names to database IDs
4. **Validation**: Field-level validation rules

---

## Key Implementation Patterns

### **1. Section-Based Architecture**
- Each section is self-contained with specific prompts
- Linear progression with ability to jump between sections
- Section completion tracked with status and scores

### **2. Structured Output Management**
```python
# Always use structured output for reliability
structured_llm = llm.with_structured_output(ChatAgentOutput, method="function_calling")
llm_output = await structured_llm.ainvoke(messages)
```

### **3. Template-Based Prompt System**
```python
# Dynamic prompt generation with data injection
system_prompt = f"{base_prompt}\\n\\n---\\n\\n{section_prompt}"
section_prompt = template.system_prompt_template.format(**canvas_data)
```

### **4. Router Directive Pattern**
```python
# Navigation control through structured directives
router_directive = "stay"        # Continue current section
router_directive = "next"        # Move to next section  
router_directive = "modify:icp"  # Jump to specific section
```

### **5. Progressive Data Collection**
```python
# Incremental field collection with validation
required_fields = ["pain1_symptom", "pain1_struggle", "pain1_cost", "pain1_consequence"]
# Only proceed when all fields collected
```

### **6. Memory Management**
```python
# Short-term conversation memory
state["short_memory"] = recent_messages[-10:]  # Keep recent context

# Long-term section memory  
state["section_states"][section_id] = SectionState(...)  # Persist section data
```

---

## Critical Success Factors

### **1. Prompts Are Everything**
- **97% of agent personality** comes from prompts
- **Conversation flow control** embedded in prompts
- **Domain expertise** expressed through prompt language
- **Output format validation** enforced in prompts

### **2. Structured Data Management**
- **Pydantic models** for type safety and validation
- **TipTap JSON** for rich text content
- **Progressive data collection** with field-level tracking
- **State persistence** across conversation sessions

### **3. LangGraph State Management**
- **State validation** at each node
- **Error recovery** and graceful degradation
- **Memory management** for conversation context
- **Tool integration** for external operations

### **4. Database Integration**
- **Section ID mapping** for external systems
- **Content serialization** to TipTap format
- **Async operations** for performance
- **Error handling** for network issues

### **5. User Experience Patterns**
- **One question at a time** for better UX
- **Progress tracking** with section completion
- **Validation and feedback** before proceeding
- **Section jumping** for flexible navigation

---

## Implementation Complexity Breakdown

| Component | Lines of Code | Complexity | Description |
|-----------|---------------|------------|-------------|
| **prompts.py** | 1,438 | 🔴 High | Domain expertise, conversation flows |
| **agent.py** | 1,107 | 🟡 Medium | LangGraph implementation (copy pattern) |
| **tools.py** | 735 | 🟡 Medium | External integrations (adapt to domain) |
| **models.py** | 396 | 🟢 Low | Data structures (follow same pattern) |

**Total**: 3,676 lines of highly structured, domain-specific code.

---

## Conclusion

The Value Canvas Agent is a sophisticated implementation that demonstrates:

1. **Complex Domain Logic**: 9 sections with detailed conversation flows
2. **Robust State Management**: Comprehensive data tracking and validation  
3. **Flexible Navigation**: User can jump between sections freely
4. **Rich Content**: TipTap integration for formatted output
5. **Database Integration**: Persistent storage with external API
6. **Error Handling**: Comprehensive logging and recovery

**For Mission Agent Implementation:**
- **Copy the exact architecture** (LangGraph nodes, state management)
- **Adapt the prompts** to mission domain expertise
- **Modify data models** to mission-specific fields
- **Update tools** for mission-specific outputs
- **Keep the same patterns** for reliability and consistency

The value canvas agent provides a battle-tested template for building sophisticated conversational agents with complex domain logic and robust state management.

