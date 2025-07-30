from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from agents.mission_pitch_models import BrandArchetype, MissionPitchData, MissionPitchStep


@dataclass
class ArchetypePattern:
    """Pattern matching data for brand archetypes"""
    core_drive: str
    origin_patterns: List[str]
    example_moments: List[str]
    business_connection: str
    well_known_examples: List[str]


# Brand Archetype Database
ARCHETYPE_PATTERNS: Dict[BrandArchetype, ArchetypePattern] = {
    BrandArchetype.CHALLENGER: ArchetypePattern(
        core_drive="Disrupts status quo, fights broken systems, champions underdogs",
        origin_patterns=[
            "Standing up to authority figures or unfair rules",
            "Questioning 'the way things are done'",
            "Defending others who were being treated unfairly",
            "Refusing to accept limitations others imposed",
            "Breaking rules that didn't make sense"
        ],
        example_moments=[
            "Organizing classmates to challenge unfair school policy",
            "Refusing to follow a rule they thought was stupid",
            "Standing up to a bully picking on someone else",
            "Questioning why things had to be done a certain way"
        ],
        business_connection="Tends toward missions that disrupt industries, challenge conventional wisdom, fight for clients against established players",
        well_known_examples=["Richard Branson (Virgin)", "Sara Blakely (Spanx)", "Reed Hastings (Netflix)", "Mark Cuban (Dallas Mavericks)"]
    ),
    
    BrandArchetype.MAGICIAN: ArchetypePattern(
        core_drive="Transforms reality, makes impossible things possible, creates breakthrough solutions",
        origin_patterns=[
            "Finding unexpected solutions to problems others couldn't solve",
            "Making something work that 'shouldn't' work",
            "Creating results that seemed impossible to others",
            "Combining unlikely elements in new ways",
            "Believing in possibilities others couldn't see"
        ],
        example_moments=[
            "Fixing something everyone said was broken beyond repair",
            "Creating an invention or solution no one expected to work",
            "Finding a way around a problem adults couldn't solve",
            "Making something happen others said was impossible"
        ],
        business_connection="Tends toward missions about transformation, breakthrough results, turning around 'impossible' situations",
        well_known_examples=["Steve Jobs (Apple)", "Tony Robbins", "Oprah Winfrey", "Elon Musk (Tesla/SpaceX)"]
    ),
    
    BrandArchetype.HERO: ArchetypePattern(
        core_drive="Overcomes obstacles through determination, proves worthiness through trials, rescues others",
        origin_patterns=[
            "Facing significant challenges and finding inner strength",
            "Overcoming personal limitations or setbacks",
            "Persisting when others would have given up",
            "Taking on difficult responsibilities others avoided",
            "Proving themselves through achievement"
        ],
        example_moments=[
            "Mastering something despite being told they couldn't",
            "Taking care of family during difficult times",
            "Overcoming personal fear or limitation",
            "Achieving something despite significant obstacles"
        ],
        business_connection="Tends toward missions about helping clients overcome challenges, achieve difficult goals, reach their potential",
        well_known_examples=["Serena Williams", "Michael Jordan", "Arnold Schwarzenegger", "Malala Yousafzai"]
    ),
    
    BrandArchetype.EXPLORER: ArchetypePattern(
        core_drive="Seeks freedom and independence, pioneers new paths, discovers possibilities",
        origin_patterns=[
            "Breaking away from limitations or expectations",
            "Venturing into unknown territory (literally or figuratively)",
            "Discovering new ways of doing things",
            "Resisting being boxed in or categorized",
            "Finding opportunities others didn't see"
        ],
        example_moments=[
            "Exploring places others were afraid to go",
            "Starting something completely new in their environment",
            "Refusing to be limited by others' expectations",
            "Discovering hidden talents or interests"
        ],
        business_connection="Tends toward missions about freedom, independence, pioneering new approaches, opening new markets",
        well_known_examples=["Bear Grylls", "Anthony Bourdain", "Jeff Bezos (Amazon/Blue Origin)", "Amelia Earhart"]
    ),
    
    BrandArchetype.SAGE: ArchetypePattern(
        core_drive="Seeks truth and understanding, shares wisdom with others, makes complex things clear",
        origin_patterns=[
            "Learning something important and feeling compelled to share it",
            "Understanding complex concepts others found difficult",
            "Teaching or explaining things to peers",
            "Solving puzzles or figuring out how things work",
            "Being the one others came to for understanding"
        ],
        example_moments=[
            "Becoming the person other kids asked to explain things",
            "Figuring out how something worked that confused others",
            "Teaching skills to friends or siblings",
            "Being recognized for understanding something complex"
        ],
        business_connection="Tends toward missions about education, consulting, making complex things simple, sharing expertise",
        well_known_examples=["Warren Buffett", "Bill Gates (Microsoft)", "Marie Curie", "Stephen Hawking"]
    ),
    
    BrandArchetype.CREATOR: ArchetypePattern(
        core_drive="Builds meaningful things, brings visions to life, expresses ideas tangibly",
        origin_patterns=[
            "Making something from nothing",
            "Building or creating physical things",
            "Bringing ideas into reality",
            "Organizing people or resources to create something",
            "Having a vision and making it happen"
        ],
        example_moments=[
            "Building something impressive with their hands",
            "Organizing an event or project that brought people together",
            "Creating art, writing, or other expressions that moved people",
            "Starting a club, business, or organization"
        ],
        business_connection="Tends toward missions about building, creating, developing, bringing visions to life",
        well_known_examples=["Martha Stewart", "James Dyson (Dyson)", "Coco Chanel", "Walt Disney"]
    ),
    
    BrandArchetype.CAREGIVER: ArchetypePattern(
        core_drive="Protects and cares for others, creates safety and security, serves needs",
        origin_patterns=[
            "Taking care of others who needed help",
            "Ensuring everyone was included and felt safe",
            "Noticing when people were struggling and intervening",
            "Creating harmony in difficult situations",
            "Putting others' needs before their own"
        ],
        example_moments=[
            "Taking care of siblings or friends during difficult times",
            "Making sure no one was left out or forgotten",
            "Mediating conflicts between others",
            "Helping people who were struggling"
        ],
        business_connection="Tends toward missions about service, protection, care, ensuring client success and security",
        well_known_examples=["Mother Teresa", "Melinda Gates (Gates Foundation)", "Marc Benioff (Salesforce)", "Princess Diana"]
    ),
    
    BrandArchetype.RULER: ArchetypePattern(
        core_drive="Creates order and structure, takes responsibility for outcomes, leads through example",
        origin_patterns=[
            "Naturally taking charge in chaotic situations",
            "Organizing people and resources effectively",
            "Taking responsibility when others wouldn't",
            "Creating systems that made things work better",
            "Being looked to for leadership and decisions"
        ],
        example_moments=[
            "Organizing other kids during group activities",
            "Taking charge during emergencies or chaos",
            "Creating systems that helped groups function better",
            "Being elected or appointed to leadership roles"
        ],
        business_connection="Tends toward missions about leadership, organization, creating order, systematic improvement",
        well_known_examples=["Jack Welch (GE)", "Margaret Thatcher", "Tim Cook (Apple)", "Indra Nooyi (PepsiCo)"]
    )
}


class ResistancePattern(Enum):
    """Common resistance patterns in Mission Pitch development"""
    TOO_PERSONAL = "too_personal_for_business"
    STORY_NOT_GOOD_ENOUGH = "story_not_good_enough"
    NOT_QUALIFIED = "not_qualified_important_enough"
    TOO_VAGUE = "too_vague_fluffy"
    PERFECTIONISM = "cant_get_perfect"


RESISTANCE_RESPONSES: Dict[ResistancePattern, Dict[str, str]] = {
    ResistancePattern.TOO_PERSONAL: {
        "signs": "Navel-gazing, too touchy-feely, how is this business relevant?",
        "core_response": "Emphasize that people buy from people, not businesses. Personal background creates real connection - think of any biography you admire, they all start with early years.",
        "key_phrases": [
            "People buy from people. Personal stories create real connection, not just transactions",
            "Every biography starts with personal background - this isn't an accident",
            "The whole point is it's NOT business-related - that's what gives you depth and makes you interesting",
            "Key People of Influence are up to something beyond just making money"
        ]
    },
    
    ResistancePattern.STORY_NOT_GOOD_ENOUGH: {
        "signs": "Nothing dramatic happened, my story is boring, comparing to others",
        "core_response": "Emphasize authenticity over drama. Small moments that felt significant to them are more powerful than big trauma.",
        "key_phrases": [
            "Small moments that felt significant to you are more powerful than big trauma",
            "Dan's story is about organizing a garage sale—relatability beats drama",
            "This isn't about being a hero - just recognizing a genuine theme through your life",
            "You're standing on a mountain of value - your stories, experiences, and perspective matter"
        ]
    },
    
    ResistancePattern.NOT_QUALIFIED: {
        "signs": "Who am I to change the world? My mission isn't important enough, shrinking vision",
        "core_response": "Address imposter syndrome by reframing scale and impact. They're describing what they'd contribute to if thousands of similar people were working toward the same thing.",
        "key_phrases": [
            "You're describing what happens when thousands with similar missions pull in the same direction",
            "Someone's mission is to help hamsters with skin problems using essential oils—that's valid if authentic",
            "Your mission needs to be specific to what YOU do, not world-saving"
        ]
    },
    
    ResistancePattern.TOO_VAGUE: {
        "signs": "Generic language, 'help people get to next level,' avoiding specifics",
        "core_response": "Push for specifics and real outcomes. Challenge them to get more precise about what actually changes.",
        "key_phrases": [
            "You're too fuzzy here. We need to get more specific",
            "What exactly is 'next level'? What would they be celebrating achieving?",
            "Vague goals don't motivate anyone or create real direction"
        ]
    },
    
    ResistancePattern.PERFECTIONISM: {
        "signs": "Won't test until perfect, over-editing, analysis paralysis",
        "core_response": "Emphasize market testing over perfection. The goal is getting close enough to have confidence in real conversations.",
        "key_phrases": [
            "The words we create here won't be the words you use in real life - that's completely normal",
            "Dan never says his Mission Pitch the same way twice", 
            "Prolific beats perfect - getting it roughly right and testing beats trying to perfect it",
            "We test in the market, not in your mind"
        ]
    }
}


def identify_archetype(personal_origin_story: str, theme: str) -> Tuple[BrandArchetype, float]:
    """
    Identify the most likely brand archetype based on personal origin story and theme.
    
    Args:
        personal_origin_story: The user's personal origin story
        theme: The user's distilled theme
        
    Returns:
        Tuple of (most_likely_archetype, confidence_score)
    """
    story_lower = personal_origin_story.lower()
    theme_lower = theme.lower()
    
    archetype_scores = {}
    
    for archetype, pattern in ARCHETYPE_PATTERNS.items():
        score = 0
        
        # Check origin patterns
        for origin_pattern in pattern.origin_patterns:
            pattern_keywords = origin_pattern.lower().split()
            if any(keyword in story_lower for keyword in pattern_keywords):
                score += 1
                
        # Check example moments
        for example in pattern.example_moments:
            example_keywords = example.lower().split()
            if any(keyword in story_lower for keyword in example_keywords):
                score += 0.5
                
        # Check theme alignment with core drive
        drive_keywords = pattern.core_drive.lower().split()
        if any(keyword in theme_lower for keyword in drive_keywords):
            score += 1
            
        archetype_scores[archetype] = score
    
    # Find the archetype with highest score
    best_archetype = max(archetype_scores, key=archetype_scores.get)
    max_score = archetype_scores[best_archetype]
    
    # Calculate confidence (normalize by maximum possible score)
    confidence = min(max_score / 3.0, 1.0)  # 3.0 is roughly max possible score
    
    return best_archetype, confidence


def get_archetype_explanation(archetype: BrandArchetype, personal_story: str, theme: str) -> str:
    """
    Generate explanation of how the user's story aligns with their identified archetype.
    
    Args:
        archetype: The identified brand archetype
        personal_story: User's personal origin story
        theme: User's distilled theme
        
    Returns:
        Formatted explanation string
    """
    pattern = ARCHETYPE_PATTERNS[archetype]
    
    explanation = f"""**The {archetype.value.title()}**: {pattern.core_drive}

Your story about {personal_story[:100]}{'...' if len(personal_story) > 100 else ''} shows the classic {archetype.value.title()} pattern. This archetype typically drives missions about {pattern.business_connection.lower()}, which aligns perfectly with your theme '{theme}'.

**Well-known {archetype.value.title()} examples**: {', '.join(pattern.well_known_examples)}

This means your origin story isn't just personal history - it's the foundation of powerful brand positioning that would resonate strongly in your market."""
    
    return explanation


def detect_resistance_pattern(user_message: str) -> Optional[ResistancePattern]:
    """
    Detect resistance patterns in user messages.
    
    Args:
        user_message: The user's message content
        
    Returns:
        Detected resistance pattern or None
    """
    message_lower = user_message.lower()
    
    # Check for resistance indicators
    resistance_indicators = {
        ResistancePattern.TOO_PERSONAL: [
            "touchy-feely", "too personal", "business relevant", "navel-gazing"
        ],
        ResistancePattern.STORY_NOT_GOOD_ENOUGH: [
            "boring", "nothing dramatic", "not interesting", "ordinary", "better story"
        ],
        ResistancePattern.NOT_QUALIFIED: [
            "who am i", "not important enough", "not qualified", "change the world"
        ],
        ResistancePattern.TOO_VAGUE: [
            "vague", "fuzzy", "not specific", "generic", "help people"
        ],
        ResistancePattern.PERFECTIONISM: [
            "not perfect", "not ready", "need to fix", "not good enough"
        ]
    }
    
    for pattern, indicators in resistance_indicators.items():
        if any(indicator in message_lower for indicator in indicators):
            return pattern
    
    return None


def get_resistance_response(pattern: ResistancePattern, user_context: str = "") -> str:
    """
    Get appropriate response for detected resistance pattern.
    
    Args:
        pattern: The detected resistance pattern
        user_context: Additional context about the user's situation
        
    Returns:
        Appropriate response string
    """
    response_data = RESISTANCE_RESPONSES[pattern]
    
    response = f"""You're not alone in feeling this way. I've been trained on hundreds of these conversations, and what you're experiencing is completely normal. Let me help you work through this.

{response_data['core_response']}

Remember: {response_data['key_phrases'][0]}"""
    
    return response


def validate_step_completion(step: MissionPitchStep, data: MissionPitchData) -> Tuple[bool, str]:
    """
    Validate if a step has been completed satisfactorily.
    
    Args:
        step: The Mission Pitch step to validate
        data: Current Mission Pitch data
        
    Returns:
        Tuple of (is_complete, validation_message)
    """
    validation_checks = {
        MissionPitchStep.HIDDEN_THEME: (
            data.distilled_theme is not None and data.theme_confidence and data.theme_confidence >= 3,
            "Theme must be distilled and user confidence must be 3 or higher"
        ),
        MissionPitchStep.PERSONAL_ORIGIN: (
            data.personal_origin_story is not None and data.origin_satisfaction and data.origin_satisfaction >= 3,
            "Personal origin story must be developed and satisfaction must be 3 or higher"
        ),
        MissionPitchStep.BUSINESS_ORIGIN: (
            data.business_origin_story is not None and data.business_satisfaction and data.business_satisfaction >= 3,
            "Business origin story must be developed and satisfaction must be 3 or higher"
        ),
        MissionPitchStep.MISSION: (
            data.mission_statement is not None and data.mission_alignment and data.mission_alignment >= 4,
            "Mission statement must be defined and alignment must be 4 or higher"
        ),
        MissionPitchStep.THREE_YEAR_VISION: (
            data.three_year_vision is not None and data.vision_satisfaction and data.vision_satisfaction >= 3,
            "3-year vision must be developed and satisfaction must be 3 or higher"
        ),
        MissionPitchStep.BIG_VISION: (
            data.big_vision is not None and data.big_vision_satisfaction and data.big_vision_satisfaction >= 3 and data.selfless_test_passed,
            "Big vision must be developed, satisfaction 3+, and selfless test passed"
        )
    }
    
    is_complete, message = validation_checks.get(step, (True, "Step validation not defined"))
    return is_complete, message


def generate_complete_mission_pitch(data: MissionPitchData) -> str:
    """
    Generate the complete Mission Pitch story from all collected data.
    
    Args:
        data: Complete Mission Pitch data
        
    Returns:
        Formatted Mission Pitch story
    """
    if not all([
        data.personal_origin_story,
        data.business_origin_story, 
        data.mission_statement,
        data.three_year_vision,
        data.big_vision
    ]):
        return "Mission Pitch is incomplete. Please complete all steps first."
    
    story = f"""**Your Complete Mission Pitch:**

**Personal Origin:** {data.personal_origin_story}

**Business Origin:** {data.business_origin_story}

**Mission:** {data.mission_statement}

**3-Year Vision:** {data.three_year_vision}

**Big Vision:** {data.big_vision}

**Thematic Connection:** Your theme '{data.distilled_theme}' runs consistently from your earliest memory through to your vision for transforming the world. This shows your entire journey—from personal experience to business mission to global impact—is genuinely connected.

---

**90-Second Conversational Flow:**
{data.personal_origin_story} This taught me {data.distilled_theme}. Years later, {data.business_origin_story} showed me this needed to become a business. Now, my mission is to {data.mission_statement}. In three years, we're celebrating that {data.three_year_vision}. But ultimately, {data.big_vision}.

Your Mission Pitch is ready for market testing. Remember: we test in the market, not in your mind. The real validation comes from how people respond when you share this story in real conversations."""
    
    return story


def get_testing_guidelines() -> str:
    """Get guidelines for testing the Mission Pitch in real conversations"""
    return """**Mission Pitch Testing Guidelines:**

**What to Listen For:**

*Story Recognition:*
- Can you tell this naturally without it feeling forced or rehearsed?
- Do people respond with 'tell me more' or do they give polite nods?
- Does it feel like your story?

*Audience Response:*
- What part creates the strongest connection with listeners?
- Where do people's eyes light up or where do they seem to tune out?
- How do different audiences respond to different elements?

*Impact Assessment:*
- Does your Mission Pitch show you're aligned to meaningful change?
- Would you want to work with someone who told a similar story?
- Does it make people want to support what you're building?

**Remember:** The words you created here won't be exactly what you use in real life—that's completely normal. This isn't a script to memorize, it's the natural arc of your story that you can tell conversationally.

**Success Indicator:** When you get this right, conversations change. Instead of having to convince people you're worth listening to, they lean in and ask 'tell me more.' That's the power of mission clarity and authentic storytelling working together."""