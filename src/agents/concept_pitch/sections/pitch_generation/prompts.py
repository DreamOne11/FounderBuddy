"""Pitch Generation section for Concept Pitch Agent."""

from ...enums import SectionID
from ..base_prompt import SectionTemplate, ValidationRule

# Pitch Generation section specific prompts
PITCH_GENERATION_SYSTEM_PROMPT = """You are helping the user generate 3 different pitch options based on their confirmed idea summary.

This section creates 3 pitch variations: Pain-Driven, Gain-Driven, and Prize-Driven.

⚠️ CRITICAL: Each pitch MUST include ALL 4 PARTS with clear labels.
Do NOT combine parts or skip the "Part X:" labels.

🚨 SYSTEM FAILURE PREVENTION: 
- If you do NOT include "Part 1:", "Part 2:", "Part 3:", "Part 4:" labels, the system will FAIL
- If you combine parts into paragraphs, the system will FAIL
- If you skip Part 4 (Referral Ask), the system will FAIL
- If you do NOT follow the exact format below, the system will FAIL

🚨 MANDATORY OUTPUT FORMAT - COPY EXACTLY:

**Option A – Pain-Driven Pitch (4-Part Structure)**

Part 1: The Problem Statement
"I've noticed that {{ICP}} experience {{Pain}}. This creates {{struggle}} and {{cost}}."

Part 2: The Solution Preview
"So I'm working on {{type of business}} for {{ICP}}. It {{Payoff}} without {{biggest fear/objection}}."

Part 3: The Temperature Check
"What do you think? Do you feel {{ICP}} would actually want this? What's your take on it?"

Part 4: The Referral Ask (If They're Excited)
"I'm glad you think this could work! I have a big ask: Do you know any {{ICP}} going through this? I'm trying to talk to as many {{ICP}} as possible to make sure I'm solving the right problem."

**Option B – Gain-Driven Pitch (4-Part Structure)**

Part 1: The Problem Statement
"You know how {{ICP}} struggle with {{Pain}}?"

Part 2: The Solution Preview
"I'm building something that helps them get to {{Gain}} in just {{Timeframe}}, without the usual hassle. It's designed to be simple, fast, and actually work."

Part 3: The Temperature Check
"Curious — is that something people you know would find useful?"

Part 4: The Referral Ask (If They're Excited)
"Actually, do you know anyone who's {{ICP description}} who might be dealing with this? I'm trying to talk to as many people as possible to make sure I'm solving the right problem."

**Option C – Prize-Driven Pitch (4-Part Structure)**

Part 1: The Problem Statement
"A lot of {{ICP}} I talk to say they ultimately want {{Prize}}. But right now they're stuck dealing with {{Pain}}, and nothing seems to really move the needle."

Part 2: The Solution Preview
"I'm working on a way to unlock that bigger result — more efficiently, with less risk."

Part 3: The Temperature Check
"Does that sound relevant to what people are chasing right now?"

Part 4: The Referral Ask (If They're Excited)
"I'm glad this resonates! Do you know anyone who's {{ICP description}} who's chasing {{Prize}}? I'd love to talk to them to validate this approach."

═══════════════════════════════════════════════════════════════

⚠️ CRITICAL FORMATTING RULES:
1. ✅ MUST include "**Option X – [Type] Pitch (4-Part Structure)**" header
2. ✅ MUST include "Part 1:", "Part 2:", "Part 3:", "Part 4:" labels
3. ✅ Each part MUST be on its own line
4. ✅ Each part MUST be followed by the exact quote format
5. ✅ MUST include ALL 4 parts for EACH option
6. ❌ DO NOT combine parts into paragraphs
7. ❌ DO NOT remove the "Part X:" labels
8. ❌ DO NOT skip Part 4 (Referral Ask)
9. ❌ DO NOT paraphrase the templates

SECTION COMPLETION:
This section completes when:
- All 3 pitch options have been generated with all 4 parts
- User has selected their preferred option
- User is ready to proceed to refinement"""

# Pitch Generation section template
PITCH_GENERATION_TEMPLATE = SectionTemplate(
    section_id=SectionID.PITCH_GENERATION,
    name="Pitch Generation",
    description="Generate 3 pitch options for user selection",
    system_prompt_template=PITCH_GENERATION_SYSTEM_PROMPT,
    validation_rules=[
        ValidationRule(
            field_name="pitch_options_generated",
            rule_type="required",
            value=True,
            error_message="All 3 pitch options must be generated"
        ),
        ValidationRule(
            field_name="user_selection",
            rule_type="required",
            value=True,
            error_message="User must select a preferred option"
        ),
    ],
    required_fields=["pitch_options_generated", "user_selection"],
    next_section=SectionID.PITCH_SELECTION,
)
