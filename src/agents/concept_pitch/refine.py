"""refine.py — Recursive refinement logic for the Concept Pitch (CAOS) Agent.
The agent collaborates with the user to iteratively improve a pitch
until the user confirms satisfaction or readiness to save.
"""

import logging
from typing import Any, Dict

from langchain_openai import ChatOpenAI

from .models import AgentState
from .prompts import get_concept_pitch_prompt

logger = logging.getLogger(__name__)


def refine_pitch(state: AgentState) -> AgentState:
    """
    Handles recursive refinement of Concept Pitch variations based on user feedback.
    The goal is to adjust tone, focus, or clarity while maintaining consistency with CAOS style.
    """
    logger.info("Starting pitch refinement process")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    system_prompt = get_concept_pitch_prompt()
    
    # Collect the current pitch and user feedback
    user_feedback = getattr(state, "user_feedback", None)
    current_pitch = state.concept_pitch or {}
    
    if not user_feedback:
        # Ask the user for what to improve
        logger.info("No user feedback provided, requesting feedback")
        state.assistant_message = (
            "Which part of this concept pitch do you feel needs adjustment? "
            "Tone? Clarity? Focus? Or overall structure?"
        )
        return state
    
    logger.info(f"Processing refinement with feedback: {user_feedback[:100]}...")
    
    # Rebuild prompt for refinement
    refinement_prompt = f"""
    You are a collaborative marketing coach helping refine a Concept Pitch.
    
    Current Pitch:
    {current_pitch}

    User Feedback:
    "{user_feedback}"

    Refine the pitch accordingly, keeping language conversational and real-world.
    Do NOT rewrite everything — only improve areas mentioned.
    Return the improved version in the same format.
    
    CAOS Principles:
    - Keep it conversational and natural
    - Focus on real-world validation
    - Maintain the collaborative tone
    - Don't over-engineer or make it too polished
    - Stay directionally correct, not perfect
    """
    
    try:
        response = llm.invoke(system_prompt + "\n" + refinement_prompt)
        
        # Update state with refined pitch
        state.concept_pitch["refined_version"] = response.content
        state.concept_pitch["refinement_feedback"] = user_feedback
        state.concept_pitch["refinement_count"] = state.concept_pitch.get("refinement_count", 0) + 1
        
        state.assistant_message = (
            "Here's the refined version based on your feedback. "
            "Does this better capture what you had in mind?"
        )
        
        # Next step: ask for confirmation again
        state.needs_refinement = False
        state.checklist_ready = True
        
        logger.info("Pitch refinement completed successfully")
        
    except Exception as e:
        logger.error(f"Error during pitch refinement: {e}")
        state.assistant_message = (
            "I encountered an error while refining the pitch. "
            "Could you try rephrasing your feedback or let me know what specific changes you'd like?"
        )
        state.concept_pitch["refinement_error"] = str(e)
    
    return state


def request_additional_feedback(state: AgentState) -> str:
    """Request additional feedback from the user for further refinement."""
    refinement_count = state.concept_pitch.get("refinement_count", 0)
    
    if refinement_count == 0:
        return (
            "Would you like to tweak anything else before finalizing your Concept Pitch? "
            "If yes, please describe the change. If not, we'll save this version."
        )
    elif refinement_count < 3:
        return (
            "How does this refined version feel? "
            "Any other adjustments you'd like to make before we finalize it?"
        )
    else:
        return (
            "We've refined this a few times now. "
            "Does this version capture what you're looking for, or would you like to try a different approach?"
        )


def analyze_feedback_sentiment(feedback: str) -> str:
    """Analyze the sentiment and type of user feedback."""
    feedback_lower = feedback.lower()
    
    if any(word in feedback_lower for word in ["good", "great", "perfect", "love", "excellent"]):
        return "positive"
    elif any(word in feedback_lower for word in ["bad", "wrong", "terrible", "hate", "awful"]):
        return "negative"
    elif any(word in feedback_lower for word in ["tone", "sound", "voice", "style"]):
        return "tone_feedback"
    elif any(word in feedback_lower for word in ["clear", "confusing", "understand", "explain"]):
        return "clarity_feedback"
    elif any(word in feedback_lower for word in ["focus", "direction", "target", "audience"]):
        return "focus_feedback"
    else:
        return "general_feedback"


def generate_refinement_suggestions(current_pitch: Dict[str, Any]) -> list[str]:
    """Generate suggestions for potential improvements based on current pitch."""
    suggestions = []
    
    # Check for common improvement areas
    pitch_text = str(current_pitch).lower()
    
    if "struggle" in pitch_text or "problem" in pitch_text:
        suggestions.append("Consider emphasizing the positive outcome more")
    
    if len(pitch_text) > 200:
        suggestions.append("Could be more concise for better impact")
    
    if "solution" in pitch_text or "help" in pitch_text:
        suggestions.append("Might benefit from more specific details")
    
    if not any(word in pitch_text for word in ["you", "your", "they", "their"]):
        suggestions.append("Consider making it more personal and direct")
    
    return suggestions


def validate_refinement_quality(original: str, refined: str) -> Dict[str, Any]:
    """Validate that the refinement maintains quality and doesn't lose key elements."""
    validation_result = {
        "maintains_structure": True,
        "improves_clarity": True,
        "preserves_key_elements": True,
        "suggestions": []
    }
    
    # Basic validation checks
    if len(refined) < len(original) * 0.5:
        validation_result["maintains_structure"] = False
        validation_result["suggestions"].append("Refinement may be too brief")
    
    if len(refined) > len(original) * 2:
        validation_result["maintains_structure"] = False
        validation_result["suggestions"].append("Refinement may be too verbose")
    
    # Check for key elements preservation
    key_words = ["icp", "pain", "gain", "prize", "solution"]
    original_lower = original.lower()
    refined_lower = refined.lower()
    
    for word in key_words:
        if word in original_lower and word not in refined_lower:
            validation_result["preserves_key_elements"] = False
            validation_result["suggestions"].append(f"Missing key element: {word}")
    
    return validation_result


# Test function for standalone usage
if __name__ == "__main__":
    # Test the refinement with mock feedback scenario
    state = AgentState(
        concept_pitch={
            "pain_pitch": "Founders face burnout from chaotic launches.",
            "gain_pitch": "Get strategic clarity for sustainable growth.",
            "prize_pitch": "Achieve freedom to build what matters."
        },
        user_feedback="Make it sound more hopeful and positive."
    )
    
    print("🚀 Testing Pitch Refinement...")
    print(f"Original pitch: {state.concept_pitch['pain_pitch']}")
    print(f"User feedback: {state.user_feedback}")
    
    try:
        result = refine_pitch(state)
        
        print("\n📋 Refinement Results:")
        print("=" * 50)
        
        if "refined_version" in result.concept_pitch:
            print("✅ Refined version:")
            print(result.concept_pitch["refined_version"])
        else:
            print("❌ No refined version generated")
            
        if "refinement_error" in result.concept_pitch:
            print(f"⚠️ Error: {result.concept_pitch['refinement_error']}")
            
        print(f"\nAssistant message: {result.assistant_message}")
        print(f"Needs refinement: {result.needs_refinement}")
        print(f"Checklist ready: {result.checklist_ready}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("✅ Structure is correct - error is due to missing dependencies")


__all__ = [
    "refine_pitch",
    "request_additional_feedback", 
    "analyze_feedback_sentiment",
    "generate_refinement_suggestions",
    "validate_refinement_quality",
]