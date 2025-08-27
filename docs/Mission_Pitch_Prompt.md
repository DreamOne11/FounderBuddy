
# Mission Pitch Agent - Complete Implementation Analysis

## Overview

This document maps the **Value Canvas Agent** implementation patterns directly onto the **Mission Pitch** domain. It is a developer-facing blueprint intended to be used as the canonical reference when implementing the Mission Pitch Agent (MPA). It follows the same structure and rigor as the Value Canvas analysis so engineers can copy architecture, LangGraph flow, prompt patterns, and data models while swapping domain-specific content.

---

## Table of Contents

1. Architecture Overview
2. File Structure Analysis
3. Prompts Deep Dive
4. Data Models Architecture
5. LangGraph Flow Implementation
6. Tools & External Integration
7. Key Implementation Patterns
8. Critical Success Factors
9. Implementation Complexity & Roadmap
10. Appendix: Example Section Templates & System Prompts

---

## 1. Architecture Overview

### The LangGraph Pattern (Mission Pitch)

```
Start → Initialize → Router → Chat Agent → Memory Updater → Router
                       ↓                                    ↑
                  Implementation ←←←←←←←←←←←←←←←┘
```

Same orchestration as Value Canvas. Each node retains identical responsibilities but uses Mission Pitch domain prompts and data models.

### Core Nodes Responsibilities (Mission Pitch specifics)

1. **Initialize Node**: Ensure mission state exists (theme, personal\_origin, business\_origin, mission\_statement, three\_year\_vision, big\_vision, archetype). Seed defaults, user/thread IDs, UI params (one-question rule, rating expectations).
2. **Router Node**: Enforce strict flow: `hidden_theme → personal_origin → business_origin → mission → 3yr_vision → big_vision → implementation`. Support `stay|next|modify:<section>` directives. Load section context and provide system prompts that enforce section-specific UX rules (e.g., "only one question at a time" for certain sections).
3. **Chat Agent Node**: Domain-aware conversational engine that returns structured output (reply, router\_directive, is\_requesting\_rating, score, section\_update). Use structured output schema specialized for Mission Pitch.
4. **Memory Updater Node**: Persist TipTap JSON, extract structured fields (theme sentence, origin details, archetype), and compute section status.
5. **Implementation Node**: When all sections complete, assemble 90-second Mission Pitch, create deliverables (text variants, slide outline, social pitch snippets), export artifacts.

---

## 2. File Structure Analysis

Recommend `src/agents/mission_pitch/` with the same modular split:

```
mission_pitch/
├── __init__.py
├── agent.py             # LangGraph orchestration (router, nodes)
├── models.py            # Pydantic models: MissionPitchState, section states
├── prompts.py           # System & section prompts (domain templates)
├── tools.py             # get_context, save_section, export_pitch, archetype_lookup
├── validators.py        # Field validators & common rules
├── docs/                # docs, examples, developer notes
└── tests/               # unit + integration tests for flows
```

**Key insight**: `prompts.py` will contain the majority of domain logic and persona (Hidden Theme exercises, Ownership Reinforcement language, Resistance handlers, archetype mapping). Keep this file isolated, well-documented, and covered by tests.

---

## 3. Prompts Deep Dive

### Base Rules (Universal System Prompt)

The Mission Pitch Agent base rules should mirror the Value Canvas base rules but be adapted for tone and constraints of the Mission Pitch framework.

**Essentials to include**:

* Role: `You are a mission-discovery partner for founders — a pragmatic, compass-holding, market-focused interviewer.`
* Communication style: plain talk, no buzzwords, emotionally intelligent but not saccharine.
* One-question-at-a-time rule where applicable.
* Output philosophy: working drafts, test-in-market, avoid polished final claims.
* Must produce structured JSON response matching `MissionAgentOutput` model.

**Required Base Prompt skeleton** (high-level idea — actual text in `prompts.py`):

```
You are an AI who helps founders craft a 90-second Mission Pitch by guiding them through: Hidden Theme, Personal Origin, Business Origin, Mission, 3-Year Vision, Big Vision.
Be direct, practical, and insist on concrete specifics. Offer options, but always force a decision gateway (stay/modify/next). Validate user ownership frequently.

Your responses MUST be valid JSON of the ChatAgentOutput schema.
```

### Section-Specific Templates

**Hidden Theme Section**

* Goal: elicit a 1-sentence theme and 2-3 supporting anecdotes.
* UX rules: allow a "2–3 minute rant" input or short bullet list. Provide distilled theme suggestions (3 options) and require confidence rating >=3 to proceed.
* Validation: theme must be a single sentence, contain at least one concrete noun and one active verb, and be specific to founder's lived experience.

**Personal Origin Section**

* Goal: capture a single, specific early memory (age, setting, action, emotional aftermath).
* UX rules: exactly one clarifying question at a time; provide 2 story templates (empowerment vs. challenge) as prompts.
* Validation: must include age, setting, and a 1-line link to the theme.

**Business Origin Section**

* Goal: capture the "this should be a business" moment: pattern (inbound demand, personal solution, market gap, lightbulb).
* UX rules: require evidence that someone would pay (anecdote, metric, or repeated ask). One question at a time.

**Mission Section**

* Goal: distill into: "My mission is to \[active change] for \[ICP] so they can \[prize/outcome]."
* UX rules: If mission doesn't align to prize, redirect to prize tuning flow.

**3-Year Vision Section**

* Goal: a believable, inspiring milestone that excites the founder and is mission-aligned.
* UX rules: must be specific (numbers, audience, distribution or reach) and pass the "would your team celebrate this" check.

**Big Vision Section**

* Goal: test against the Selfless Test; must be aspirational but not purely self-aggrandizing.
* UX rules: if founder hesitates, propose scaled-down and scaled-up variants.

**Resistance Handling**\nEmbed exactly the resistance patterns from the Mission Pitch doc: "too touchy-feely", "not important", "not dramatic enough", etc. Include canned, short reframes.

**Archetype Mapping**
Implement a short mapping prompt: present top-2 archetypes and 1 "different story entirely" option with clear rationales. Require user pick or reject.

**Structured output enforcement**
Every system prompt must remind the model to return a structured `ChatAgentOutput` with: `reply`, `router_directive`, `is_requesting_rating`, `score`, `section_update` (TipTap JSON) when applicable.

---

## 4. Data Models Architecture

### Core State Model (MissionPitchState)

```python
class MissionPitchState(MessagesState):
    user_id: int
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    current_section: SectionID = SectionID.HIDDEN_THEME
    context_packet: ContextPacket | None = None
    section_states: dict[str, SectionState] = Field(default_factory=dict)
    router_directive: str = RouterDirective.NEXT
    finished: bool = False

    canvas_data: MissionPitchData = Field(default_factory=MissionPitchData)
    short_memory: list[BaseMessage] = Field(default_factory=list)

    agent_output: ChatAgentOutput | None = None
    awaiting_user_input: bool = False
    is_awaiting_rating: bool = False

    error_count: int = 0
    last_error: str | None = None
```

### Section Identifiers

```python
class SectionID(str, Enum):
    HIDDEN_THEME = "hidden_theme"
    PERSONAL_ORIGIN = "personal_origin"
    BUSINESS_ORIGIN = "business_origin"
    MISSION = "mission"
    THREE_YEAR_VISION = "three_year_vision"
    BIG_VISION = "big_vision"
    IMPLEMENTATION = "implementation"
```

### MissionPitchData

```python
class MissionPitchData(BaseModel):
    # Hidden theme
    theme_1sentence: str | None = None
    theme_rant: str | None = None
    theme_confidence: int | None = None

    # Personal origin
    personal_origin_age: int | None = None
    personal_origin_setting: str | None = None
    personal_origin_key_moment: str | None = None
    personal_origin_link_to_theme: str | None = None

    # Business origin
    business_origin_pattern: str | None = None
    business_origin_story: str | None = None
    business_origin_evidence: str | None = None

    # Mission
    mission_statement: str | None = None
    prize: str | None = None

    # 3yr Vision
    three_year_milestone: str | None = None
    three_year_metrics: dict | None = None

    # Big Vision
    big_vision: str | None = None
    big_vision_selfless_test_passed: bool | None = None

    # Archetype
    archetype_primary: str | None = None
    archetype_secondary: str | None = None

    # Metadata
    last_updated: datetime | None = None
```

### ChatAgentOutput (MissionAgentOutput)

Same structured schema as Value Canvas but mission-specific field naming and validations.

```python
class ChatAgentOutput(BaseModel):
    reply: str
    router_directive: str  # 'stay'|'next'|'modify:<section_id>'
    is_requesting_rating: bool = False
    score: int | None = None
    section_update: dict | None = None  # TipTap JSON or field updates
```

**Validation rules**: Pydantic validators must check for required fields per section before allowing `router_directive: next`.

---

## 5. LangGraph Flow Implementation

### Initialize Node

Same as Value Canvas but seed mission-specific defaults and ensure `prompts.py` templates are available. Initialize checks:

* `user_id` exists
* `thread_id` created
* default `current_section` set
* `canvas_data` fields initialized

### Router Node

Implement identical router logic but ordering is the Mission Pitch sequence. The node must call `get_context` with the `section_id` to load the correct system prompt and draft data.

Router behaviors:

* `stay`: do nothing
* `next`: find next unfinished Mission Pitch section (explicit ordering)
* `modify:<section>`: jump to section
* When setting `current_section`, load context from `get_context` and then set `router_directive = stay` so ChatAgent handles the first message.

### Chat Agent Node

Key differences from Value Canvas:

* Use a specialized LLM persona: pragmatic mission interviewer.
* Must call `with_structured_output(ChatAgentOutput)` or use function-calling/JSON schema to ensure structured outputs.
* Build `messages` including: base system prompt, section system prompt (from context\_packet), short\_memory, and the last human message.
* After `ainvoke`, set `state.agent_output = llm_output` and push `AIMessage` into `messages`.

### Memory Updater Node

When `agent_output.section_update` exists:

* Save TipTap JSON via `save_section`
* Run an `extract_structured_fields` tool (LLM-assisted extractor) that maps TipTap content to `MissionPitchData` fields (e.g., parse a Personal Origin block into age, setting, key\_moment)
* Compute `computed_status` (complete/incomplete) using validation rules
* Update `section_states[section_id]` with content, score, status, timestamp

### Implementation Node

When `state.finished == True` or when `router_directive == 'modify:implementation'`:

* Assemble the final deliverables:

  * 90-second pitch (conversational, 3 variants: short/medium/long)
  * Slide deck outline (6 slides: Hook, Theme, Personal Origin, Business Origin, Mission & 3yr Vision, Big Vision + CTA)
  * Social pitch snippets (3 tweets, 3 LinkedIn intros)
  * Speaker script bullet points and notes on where to test in market
* Provide export endpoints: `export_pitch`, `export_to_docx`, `export_to_pptx` (tools)

---

## 6. Tools & External Integration

### Core Tools (Mission Pitch)

```
router_tools = [get_context]
memory_updater_tools = [save_section, extract_structured_fields, validate_fields]
implementation_tools = [export_pitch, generate_slide_outline]
```

### get\_context (mission)

* Renders base\_prompt + section\_prompt (safe templating with `.format()` fallback to blank values)
* Returns system\_prompt, draft content, status, validation\_rules

### save\_section

* Persists TipTap JSON and minimal metadata

### extract\_structured\_fields

* Given TipTap JSON or plain text, returns structured mission fields using a schema mapping
* Implementation detail: prefer a small enclosed LLM call or regex/parsing heuristics with fallback

### export\_pitch

* Accepts assembled MissionPitchData, returns artifacts (text, slides, speaker notes)

**Integration considerations**

* Use existing DentApp API or a Postgres/Supabase table to store `section_states` and `mission_pitch` objects.
* TipTap JSON stored in a `content` column; extracted fields stored in typed columns.
* Provide idempotent `save_section` so repeated saves are safe.

---

## 7. Key Implementation Patterns (Mapping from Value Canvas)

1. **Section-Based Architecture**: Each Mission Pitch element is a self-contained section with validation and UX rules.
2. **Structured Output Management**: Always use a structured schema for Chat responses to keep router deterministic.
3. **Template-Based Prompts**: Base prompt + section prompt composition. Section prompts must include explicit UX rules (one question at a time, required fields, rating gates).
4. **Router Directive Pattern**: `stay|next|modify:<section>` same as Value Canvas.
5. **Progressive Collection**: Enforce required fields for each section; only when validated can `next` be emitted.
6. **Short & Long Memory**: Keep short memory of recent messages and persist long section data in DB.
7. **Archetype Mapping Reuse**: Use the archetype list from Mission Pitch doc; present top-2 archetypes and allow "different story entirely".
8. **Resistance & Reframe Scripts**: Hard-coded short responses to common pushback that can be invoked by the Chat Agent node.

---

## 8. Critical Success Factors

1. **Prompts Are Everything**: Mission-specific persona AND failure modes must be written into `prompts.py`.
2. **Field Validation**: Strong pydantic validators so the router never advances on incomplete sections.
3. **User Ownership Mechanisms**: Always ask for a confidence rating and present decision gateways to ensure founders own the output.
4. **Market-Testing Guidance**: Provide explicit instructions and simple A/B test suggestions when a section completes.
5. **Archetype Fit**: Archetype suggestions must be tied to verbatim user memories for credibility.
6. **Export Quality**: Final exports (90s pitch, slides) must be readable, human-sayable, and tested against the "90-second flow" in the Mission Pitch doc.

---

## 9. Implementation Complexity & Roadmap

| Component     | LOC Estimate | Complexity | Notes                                         |
| ------------- | -----------: | ---------- | --------------------------------------------- |
| prompts.py    |      \~1,200 | 🔴 High    | Domain logic & UX rules — most time-consuming |
| agent.py      |      \~1,000 | 🟡 Medium  | LangGraph nodes & wiring                      |
| tools.py      |        \~600 | 🟡 Medium  | persistence and extraction tools              |
| models.py     |        \~300 | 🟢 Low     | Pydantic models for mission state             |
| validators.py |        \~200 | 🟢 Low     | Section validators and CI checks              |
| docs + tests  |        \~400 | 🟡 Medium  | Examples, unit tests for each section         |

**Total**: \~3,700 lines (similar to Value Canvas). Prioritize `prompts.py` and `extract_structured_fields` tool.

### Suggested Implementation Roadmap (8 weeks fast-track)

1. **Week 0–1**: Scaffold repository, models.py, and initial router.
2. **Week 1–3**: Implement `prompts.py` sections (Hidden Theme, Personal Origin, Business Origin). Build tests for one-question UX rules.
3. **Week 3–4**: Implement Chat Agent node and structured output plumbing. Add `get_context` tool.
4. **Week 4–5**: Implement Memory Updater + `save_section` + `extract_structured_fields` (LLM-assisted mapping).
5. **Week 5–6**: Implement Mission, 3yr Vision, Big Vision sections, archetype mapping logic.
6. **Week 6–7**: Implement Implementation Node + `export_pitch` + slide outline generator.
7. **Week 7–8**: End-to-end testing, UX polish, and documentation.

---

## 10. Appendix: Example Section Templates & System Prompts

*(This appendix contains representative templates and JSON schemas for the ChatAgentOutput and SectionState. Keep these small and representative — full templates belong inside `prompts.py`.)*

### Example: Hidden Theme system prompt (abridged)

```
SYSTEM: Hidden Theme section.
You will: - Ask the user to "choose a sentence starter" that sparks a 2-3 minute rant. - After the rant, produce 3 distilled theme options (each ≤ 20 words). - Ask the user to rate confidence 0–5 and pick one option.

UX RULES:
- Ask only one question at a time.
- If confidence < 3, offer small refinement questions and do not allow next.

OUTPUT: Return ChatAgentOutput with section_update containing TipTap JSON of the chosen theme and the other options.
```

### Example: ChatAgentOutput JSON (Mission)

```json
{
  "reply": "Here are three theme options based on what you said...",
  "router_directive": "stay",
  "is_requesting_rating": true,
  "score": null,
  "section_update": {
    "content": [{"type":"paragraph","children":[{"text":"Theme option 1: ..."}]}]
  }
}
```

---

## Conclusion

This analysis translates the Value Canvas implementation into a Mission Pitch specialization. The major lift is writing robust, tested `prompts.py` content and building the `extract_structured_fields` tool that reliably maps freeform inputs into the `MissionPitchData` model. Keep the same LangGraph architecture, enforce strict validation gates, and prioritize founder ownership and market-testing in every section.

### Deliverables you can extract from this blueprint

* Full repo skeleton
* `prompts.py` contents for each section
* `models.py` and validators
* LangGraph nodes (`agent.py`) wired to tools
* Tools: `get_context`, `save_section`, `extract_structured_fields`, `export_pitch`

If you want, I can now:

* Generate the full `models.py` and `agent.py` stubs,
* Produce the complete `prompts.py` with the Mission Pitch system prompts and templates,
* Or generate sample TipTap JSON examples and unit test skeletons.

Which output would you like me to create next?
