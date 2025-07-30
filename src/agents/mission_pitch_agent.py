from datetime import datetime
from typing import Literal, Dict, Any, List, Optional
import json

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.managed import RemainingSteps
from pydantic import BaseModel, Field

from agents.llama_guard import LlamaGuard, LlamaGuardOutput, SafetyAssessment
from agents.mission_pitch_models import MissionPitchStep, BrandArchetype, MissionPitchData
from agents.mission_pitch_tools import (
    identify_archetype, get_archetype_explanation, detect_resistance_pattern,
    get_resistance_response, validate_step_completion, generate_complete_mission_pitch,
    get_testing_guidelines, ARCHETYPE_PATTERNS
)
from core import get_model, settings
from core.db import get_user_context




class AgentState(MessagesState, total=False):
    """State for Mission Pitch Agent"""
    safety: LlamaGuardOutput
    remaining_steps: RemainingSteps
    user_id: str | None
    mission_pitch_data: MissionPitchData
    awaiting_user_input: bool
    current_question: str | None


# Main system prompt for the Mission Pitch Agent
MISSION_PITCH_SYSTEM_PROMPT = """You are an AI Agent specifically designed to help business owners develop their Mission Pitch—an authentic story that connects your origin, mission and vision in under two minutes.

## Core Understanding

The Mission Pitch transforms everyday introductions into opportunities to show you're a leader with real purpose beyond just making money. Without this story, you sound like every other service provider instead of a leader worth following.

The Mission Pitch connects six elements into one compelling narrative:
1. **Hidden Theme** - The consistent thread running through your life
2. **Personal Origin** - Early moment that revealed your passion/theme  
3. **Business Origin** - "This should be a business" realization
4. **Mission** - Daily North Star (turning client's pain into transformation)
5. **3-Year Vision** - Specific business milestone you're working toward
6. **Big Vision** - Selfless world transformation you want to help create

## Your Role: Intellectual Co-Creation

**Guide decisions that shape their story, not create it for them.**

### Language Framework:
- "Given your insight about X, I've developed this approach..."
- "Based on your unique experience with Y, this direction aligns with your approach..."
- "Your perspective on Z is what makes this remarkable rather than generic"

### Decision Gateways: 
Create explicit choice points requiring their input:
- "I see two directions here. Option A emphasizes [X], Option B highlights [Y]. Which better aligns with your genuine experience?"
- "This could show you as [identity A] or [identity B]. Which feels more true to who you are?"

### Insufficiency Alerts: 
When input lacks uniqueness, directly state:
- "To create something truly distinctive, I need more of YOUR specific experience here"
- "This feels generic. What unique insight have YOU discovered that others in your field miss?"

## Key Resistance Patterns & Responses

**"This feels too touchy-feely"** → "Most people I work with struggle with boring career rambles, wasting a prime opportunity to demonstrate leadership and build genuine connection. Your theme feels ordinary to you because you've lived with it—that's exactly why it's powerful to others."

**"My story is boring/nothing dramatic happened"** → "Small moments that felt significant to you are more powerful than big trauma. Dan's story is organizing a garage sale—relatability beats drama. You're standing on a mountain of value."

**"I fell into this business accidentally"** → "Every business start is valid. Your insight about that 'accident' is what makes your story compelling and distinctive."

## Required Check-Ins:
- "Do any elements of this feel awkward or uncomfortable to you?"
- "Does anything about this feel forced or manufactured?"
- "Are you finding yourself comparing your story to others?"
- "Do you have any worries about sharing this story?"

## Success Criteria:
- Users should feel confident defending and explaining their story to others
- They see themselves as the expert who simply used AI as a thinking partner
- The story feels authentically theirs, not AI-generated

Remember: We test in the market, not in your mind. The real validation comes from how people respond when you share this story in real conversations."""


async def get_system_prompt(user_id: str | None = None) -> str:
    """Generate personalized system prompt based on user context"""
    base_prompt = MISSION_PITCH_SYSTEM_PROMPT
    
    if user_id:
        try:
            user_context = await get_user_context(user_id)
            return user_context + "\n\n" + base_prompt
        except Exception as e:
            print(f"[DEBUG] Error fetching user context: {e}")
            return base_prompt
    
    return base_prompt


async def wrap_model(model: BaseChatModel, user_id: str | None = None) -> RunnableSerializable[AgentState, AIMessage]:
    """Wrap the model with system prompt and tools"""
    system_prompt = await get_system_prompt(user_id)
    
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=system_prompt)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model


def format_safety_message(safety: LlamaGuardOutput) -> AIMessage:
    """Format safety warning message"""
    content = (
        f"This conversation was flagged for unsafe content: {', '.join(safety.unsafe_categories)}"
    )
    return AIMessage(content=content)


async def initialize_mission_pitch(state: AgentState, config: RunnableConfig) -> AgentState:
    """Initialize Mission Pitch data if not present"""
    user_id = state.get("user_id") or config["configurable"].get("user_id")
    
    if "mission_pitch_data" not in state or state["mission_pitch_data"] is None:
        # Try to load existing mission data from database
        mission_data = await load_mission_pitch_data(user_id) if user_id else MissionPitchData()
        
        return {
            "mission_pitch_data": mission_data,
            "awaiting_user_input": True,
            "current_question": get_step_introduction(mission_data.current_step)
        }
    return state


async def load_mission_pitch_data(user_id: str) -> MissionPitchData:
    """Load existing Mission Pitch data for a user"""
    try:
        from core.db import supabase
        if not supabase:
            return MissionPitchData()
        
        # Try to load from a hypothetical mission_pitch_sessions table
        response = supabase.table('mission_pitch_sessions').select('*').eq('user_id', user_id).order('updated_at', desc=True).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            session_data = response.data[0]
            # Convert stored JSON back to MissionPitchData
            mission_data_json = session_data.get('mission_data', {})
            return MissionPitchData(**mission_data_json)
    except Exception as e:
        print(f"[DEBUG] Error loading mission pitch data: {e}")
    
    return MissionPitchData()


async def save_mission_pitch_data(user_id: str, mission_data: MissionPitchData) -> bool:
    """Save Mission Pitch data to database"""
    if not user_id:
        return False
        
    try:
        from core.db import supabase
        if not supabase:
            return False
        
        # Convert MissionPitchData to JSON
        mission_data_json = mission_data.dict()
        
        # Upsert to mission_pitch_sessions table
        response = supabase.table('mission_pitch_sessions').upsert({
            'user_id': user_id,
            'mission_data': mission_data_json,
            'current_step': mission_data.current_step.value,
            'updated_at': datetime.now().isoformat()
        }).execute()
        
        return True
    except Exception as e:
        print(f"[DEBUG] Error saving mission pitch data: {e}")
        return False


def get_step_introduction(step: MissionPitchStep) -> str:
    """Get introduction message for each step"""
    introductions = {
        MissionPitchStep.HIDDEN_THEME: """Let's discover your hidden theme—the consistent thread that's been running through your life, even if you've never put words to it before. This isn't about finding something impressive or commercial. It's about identifying what genuinely drives you.

Most people's passions aren't random—there's usually a consistent thread that shows up in their work, hobbies, and conversations. Your hidden theme is what you naturally gravitate toward, what you can rant about for hours, what gets you genuinely excited even when others don't see it.

Choose the sentence starter that immediately sparks something in you. Don't analyze—just pick the one that makes you want to keep talking:

1. "For as long as I can remember, I've felt there's something exciting at the intersection of _____ and _____"
2. "I deeply believe the world needs _____"  
3. "Never in history has there been a better time for _____"
4. "My whole life I've been fascinated by what happens when you mix _____ and _____"

Which of these sentence starters immediately grabs you? Or does a different version come to mind?""",

        MissionPitchStep.PERSONAL_ORIGIN: """Now let's connect your theme to its earliest appearance in your life. We're looking for a specific moment, ideally before you had commercial responsibility, where you experienced something that reveals the seed of your current passion.

Your Personal Origin doesn't need to be dramatic—the most powerful stories often come from seemingly small moments that felt significant to YOU. A quiet realization can be more compelling than surviving a catastrophe.

We're looking for the earliest moment when your theme showed up, even if you didn't have words for it then. Remember: You can't connect the dots looking forward. It's only looking back with your theme in mind that you'll recognize the significance of moments you might have overlooked.

Think about early experiences that connect to your theme. What specific moment from your past first revealed this driving force in your life?""",

        MissionPitchStep.BUSINESS_ORIGIN: """Now let's find your 'this should be a business' moment—when you realized people would actually pay for what you're passionate about.

Your Business Origin doesn't need to directly connect to your Personal Origin story. They might be separated by decades—that's completely normal. What matters is that the same theme connects them across time and space.

We're looking for the moment when you realized your passion could solve real problems for people who'd pay for solutions. Every business start is valid. Whether you stumbled into it, got fired and had no choice, started by accident, or spotted a market gap—there's no 'right' way to begin.

When exactly did you think 'this should be a business'? What made you realize there was a commercial opportunity in what you were passionate about?""",

        MissionPitchStep.MISSION: """Your mission should be almost identical to what your clients ultimately want to achieve. When these align, clients stop seeing you as just another service provider and start seeing you as someone who genuinely wants the same outcome they want.

Your mission isn't all about you. When your mission aligns with your clients' goals, they feel it. People would much rather work with a company whose founder is committed to the same outcome they want and is motivated to achieve it for reasons beyond just money.

What exact transformation do you create for your clients? Replace 'help' with the active change you produce. Your mission should be specific to YOUR expertise, not world-saving. That specificity is what makes you the obvious choice.

What is your daily North Star? What transformation are you committed to creating every day?""",

        MissionPitchStep.THREE_YEAR_VISION: """Now let's create your 3-Year Vision—the specific business milestone you're working toward that bridges the gap between where you are now and your bigger vision for the world.

Your 3-Year Vision needs to be practical, achievable, and believable while still being inspiring enough that when people hear it, they want to join you on the journey. This vision should be bigger than just money. While hitting revenue targets might matter to you personally, it's boring to mission-aligned people.

Think of it this way: in three years, you're throwing a celebration party. Your team, clients, and industry peers are all there saying 'We did it!' What specific achievement are you celebrating that goes beyond just financial success?

What milestone would genuinely excite YOU, not what sounds impressive to others?""",

        MissionPitchStep.BIG_VISION: """Congratulations! You're on the final step of your Mission Pitch. Now let's create your Big Vision—your selfless vision for the world transformation you want to help create, whether you get credit or not.

Your Big Vision demonstrates that you're aligned to something far bigger than your business, your bank account, or your personal recognition. When people hear your Big Vision, they instinctively understand that working with you isn't just a transaction—it's joining a movement.

You're not claiming you'll single-handedly transform everything. You're describing what you'd want to see happen if thousands of people with similar missions were all pulling in the same direction. You're describing the world you'd contribute to creating, not the world you'll create alone.

What world transformation do you want to help create? What would you want to see happen even if your business disappeared tomorrow and someone else made it happen instead?"""
    }
    
    return introductions.get(step, "Let's continue with the next step of your Mission Pitch.")


async def process_mission_pitch_step(state: AgentState, config: RunnableConfig) -> AgentState:
    """Process the current step of the Mission Pitch workflow"""
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    user_id = state.get("user_id") or config["configurable"].get("user_id")
    
    mission_data = state.get("mission_pitch_data", MissionPitchData())
    current_step = mission_data.current_step
    
    # Get the last user message
    last_message = state["messages"][-1] if state["messages"] else None
    if not last_message or last_message.type != "human":
        # If no user message, provide step introduction
        intro_message = get_step_introduction(current_step)
        return {
            "messages": [AIMessage(content=intro_message)],
            "awaiting_user_input": True,
            "current_question": intro_message
        }
    
    # Process user input based on current step
    user_input = last_message.content
    if isinstance(user_input, list):
        # If content is a list, join it into a string
        user_input = " ".join(str(item) for item in user_input)
    
    # Check for resistance patterns
    resistance_pattern = detect_resistance_pattern(user_input)
    if resistance_pattern:
        resistance_response = get_resistance_response(resistance_pattern, user_input)
        return {
            "messages": [AIMessage(content=resistance_response)],
            "awaiting_user_input": True
        }
    
    # Create model runnable for this specific step
    model_runnable = await wrap_model(m, user_id)
    
    # Generate step-specific prompt
    step_prompt = get_step_processing_prompt(current_step, user_input, mission_data)
    
    # Add step-specific context to state
    context_messages = [HumanMessage(content=step_prompt)]
    response = await model_runnable.ainvoke({
        "messages": state["messages"] + context_messages
    }, config)
    
    # Update mission data based on step progress
    updated_mission_data = update_mission_data(current_step, user_input, mission_data, response.content)
    
    # Save updated data to database
    if user_id:
        await save_mission_pitch_data(user_id, updated_mission_data)
    
    # Check if step is complete and should advance
    should_advance, validation_message = should_advance_step(current_step, updated_mission_data, user_input)
    
    if should_advance:
        # Advance to next step
        next_step = get_next_step(current_step)
        updated_mission_data.current_step = next_step
        
        if next_step == MissionPitchStep.COMPLETE:
            # Generate complete Mission Pitch
            complete_pitch = generate_complete_mission_pitch(updated_mission_data)
            testing_guidelines = get_testing_guidelines()
            final_message = f"{response.content}\n\n---\n\n{complete_pitch}\n\n{testing_guidelines}"
            updated_mission_data.ready_for_testing = True
            return {
                "messages": [AIMessage(content=final_message)],
                "mission_pitch_data": updated_mission_data,
                "awaiting_user_input": False
            }
        else:
            # Continue to next step
            next_intro = get_step_introduction(next_step)
            combined_message = f"{response.content}\n\n---\n\n{next_intro}"
            return {
                "messages": [AIMessage(content=combined_message)],
                "mission_pitch_data": updated_mission_data,
                "awaiting_user_input": True,
                "current_question": next_intro
            }
    
    return {
        "messages": [response],
        "mission_pitch_data": updated_mission_data,
        "awaiting_user_input": True
    }


def get_step_processing_prompt(step: MissionPitchStep, user_input: str, mission_data: MissionPitchData) -> str:
    """Generate step-specific processing prompt"""
    base_context = f"""
    Current Step: {step.value}
    User Input: {user_input}
    
    Previous Mission Pitch Data:
    - Theme: {mission_data.distilled_theme or 'Not yet defined'}
    - Personal Origin: {mission_data.personal_origin_story or 'Not yet defined'}
    - Business Origin: {mission_data.business_origin_story or 'Not yet defined'}
    - Mission: {mission_data.mission_statement or 'Not yet defined'}
    - 3-Year Vision: {mission_data.three_year_vision or 'Not yet defined'}
    """
    
    step_specific_prompts = {
        MissionPitchStep.HIDDEN_THEME: f"""
        {base_context}
        
        The user has provided their response to the theme discovery exercise. Your tasks:
        1. Help them explore their chosen sentence starter more deeply
        2. Guide them through a 2-3 minute exploration of what drives them
        3. Ask clarifying questions to help them articulate their unique perspective
        4. Once you have enough material, offer 3-4 distilled theme options
        5. Use the co-creation protocol - guide their decisions, don't create for them
        
        Remember: Their theme might feel ordinary to them because they've lived with it. That's exactly why it's powerful to others.
        """,
        
        MissionPitchStep.PERSONAL_ORIGIN: f"""
        {base_context}
        
        The user is sharing their personal origin story. Your tasks:
        1. Help them identify the specific moment when their theme first appeared
        2. Guide them to include key details: age, situation, what happened, why it mattered
        3. Connect this moment explicitly to their established theme
        4. Help them see the significance of what might seem like a small moment
        5. Once developed, check if this story feels authentic and comfortable to them
        
        Look for opportunities to identify their brand archetype based on their story patterns.
        """,
        
        MissionPitchStep.BUSINESS_ORIGIN: f"""
        {base_context}
        
        The user is developing their business origin story. Your tasks:
        1. Help them identify the exact moment they realized "this should be a business"
        2. Guide them to articulate what evidence showed people would pay for this
        3. Connect this business realization to their theme (not necessarily their personal origin)
        4. Validate that this story feels genuine and not manufactured
        5. Show how this connects thematically to their personal origin
        
        Remember: Every business start is valid, including accidents and stumbles.
        """,
        
        MissionPitchStep.MISSION: f"""
        {base_context}
        
        The user is defining their mission statement. Your tasks:
        1. Help them articulate the exact transformation they create for clients
        2. Ensure the mission aligns with what their clients want to achieve
        3. Replace vague "help" language with specific, active transformation
        4. Test that this mission genuinely excites them personally
        5. Validate that this connects to their theme and origins
        
        The mission should be specific to their expertise, not world-saving generalities.
        """,
        
        MissionPitchStep.THREE_YEAR_VISION: f"""
        {base_context}
        
        The user is creating their 3-year vision. Your tasks:
        1. Help them identify a specific business milestone worth celebrating
        2. Ensure it's bigger than just financial metrics
        3. Test that this vision would genuinely excite their team and clients
        4. Validate it feels challenging but achievable
        5. Connect it as a natural extension of their mission
        
        This should be the stepping stone that makes their eventual Big Vision feel possible.
        """,
        
        MissionPitchStep.BIG_VISION: f"""
        {base_context}
        
        The user is articulating their big vision. Your tasks:
        1. Help them describe the world transformation they want to contribute to
        2. Apply the selfless test: would they want this even if they got no credit?
        3. Ensure it's about collective impact, not individual achievement
        4. Connect it thematically to their entire story arc
        5. Validate this feels genuinely inspiring to them
        
        This is what separates true key people of influence from everyone else.
        """
    }
    
    return step_specific_prompts.get(step, base_context)


async def llama_guard_input(state: AgentState, config: RunnableConfig) -> AgentState:
    """Run LlamaGuard safety check on input"""
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("User", state["messages"])
    return {"safety": safety_output, "messages": []}


async def block_unsafe_content(state: AgentState, config: RunnableConfig) -> AgentState:
    """Block unsafe content with appropriate message"""
    safety: LlamaGuardOutput = state["safety"]
    return {"messages": [format_safety_message(safety)]}


def check_safety(state: AgentState) -> Literal["unsafe", "safe"]:
    """Check if content is safe to process"""
    safety: LlamaGuardOutput = state["safety"]
    match safety.safety_assessment:
        case SafetyAssessment.UNSAFE:
            return "unsafe"
        case _:
            return "safe"


def update_mission_data(step: MissionPitchStep, user_input: str, mission_data: MissionPitchData, ai_response: str) -> MissionPitchData:
    """Update mission data based on current step progress"""
    updated_data = MissionPitchData(**mission_data.dict())
    
    # Extract key information based on step
    if step == MissionPitchStep.HIDDEN_THEME:
        # Look for theme completion indicators in AI response
        if "theme" in ai_response.lower() and len(user_input) > 50:
            updated_data.theme_rant = user_input
            # In a real implementation, you'd parse the AI response for the distilled theme
            if "distilled theme" in ai_response.lower():
                # Extract theme from AI response (simplified)
                updated_data.distilled_theme = extract_theme_from_response(ai_response)
    
    elif step == MissionPitchStep.PERSONAL_ORIGIN:
        if len(user_input) > 100:  # Sufficient detail for a story
            updated_data.personal_origin_story = user_input
            # Identify archetype if story is complete
            if updated_data.distilled_theme:
                archetype, confidence = identify_archetype(user_input, updated_data.distilled_theme)
                if confidence > 0.5:
                    updated_data.identified_archetype = archetype
    
    elif step == MissionPitchStep.BUSINESS_ORIGIN:
        if "business" in user_input.lower() and len(user_input) > 50:
            updated_data.business_origin_story = user_input
    
    elif step == MissionPitchStep.MISSION:
        if "mission" in user_input.lower() or len(user_input) > 30:
            updated_data.mission_statement = user_input
    
    elif step == MissionPitchStep.THREE_YEAR_VISION:
        if "vision" in user_input.lower() or "years" in user_input.lower():
            updated_data.three_year_vision = user_input
    
    elif step == MissionPitchStep.BIG_VISION:
        if len(user_input) > 30:
            updated_data.big_vision = user_input
            # Check for selfless test indicators
            if "even if" in user_input.lower() or "without credit" in user_input.lower():
                updated_data.selfless_test_passed = True
    
    return updated_data


def should_advance_step(step: MissionPitchStep, mission_data: MissionPitchData, user_input: str) -> tuple[bool, str]:
    """Determine if current step is complete and should advance"""
    # Look for satisfaction ratings or completion indicators in user input
    satisfaction_indicators = ["satisfied", "good", "ready", "next", "continue", "done"]
    rating_indicators = ["4", "5", "satisfied", "confident"]
    
    user_lower = user_input.lower()
    
    # Basic completion checks
    step_complete_checks = {
        MissionPitchStep.HIDDEN_THEME: mission_data.distilled_theme is not None,
        MissionPitchStep.PERSONAL_ORIGIN: mission_data.personal_origin_story is not None,
        MissionPitchStep.BUSINESS_ORIGIN: mission_data.business_origin_story is not None,
        MissionPitchStep.MISSION: mission_data.mission_statement is not None,
        MissionPitchStep.THREE_YEAR_VISION: mission_data.three_year_vision is not None,
        MissionPitchStep.BIG_VISION: mission_data.big_vision is not None
    }
    
    # Check if basic requirements are met
    basic_complete = step_complete_checks.get(step, False)
    
    # Check for user satisfaction/advancement signals
    wants_to_advance = any(indicator in user_lower for indicator in satisfaction_indicators)
    high_satisfaction = any(indicator in user_lower for indicator in rating_indicators)
    
    should_advance = basic_complete and (wants_to_advance or high_satisfaction)
    
    message = "Step complete" if should_advance else "Continue current step"
    return should_advance, message


def get_next_step(current_step: MissionPitchStep) -> MissionPitchStep:
    """Get the next step in the Mission Pitch workflow"""
    step_order = [
        MissionPitchStep.HIDDEN_THEME,
        MissionPitchStep.PERSONAL_ORIGIN,
        MissionPitchStep.BUSINESS_ORIGIN,
        MissionPitchStep.MISSION,
        MissionPitchStep.THREE_YEAR_VISION,
        MissionPitchStep.BIG_VISION,
        MissionPitchStep.COMPLETE
    ]
    
    try:
        current_index = step_order.index(current_step)
        if current_index < len(step_order) - 1:
            return step_order[current_index + 1]
        else:
            return MissionPitchStep.COMPLETE
    except ValueError:
        return MissionPitchStep.COMPLETE


def extract_theme_from_response(ai_response: str) -> str:
    """Extract distilled theme from AI response (simplified implementation)"""
    # In a real implementation, this would use more sophisticated parsing
    # For now, return a placeholder that would be replaced by actual theme extraction
    lines = ai_response.split('\n')
    for line in lines:
        if 'theme' in line.lower() and ':' in line:
            return line.split(':', 1)[1].strip().strip('"\'')
    return "Theme to be refined"


# Define the graph
agent = StateGraph(AgentState)

# Add nodes
agent.add_node("initialize", initialize_mission_pitch)
agent.add_node("guard_input", llama_guard_input)
agent.add_node("block_unsafe_content", block_unsafe_content)
agent.add_node("process_step", process_mission_pitch_step)

# Set entry point
agent.set_entry_point("initialize")

# Add edges
agent.add_edge("initialize", "guard_input")

# Conditional edges for safety check
agent.add_conditional_edges(
    "guard_input", 
    check_safety, 
    {"unsafe": "block_unsafe_content", "safe": "process_step"}
)

# Terminal edges
agent.add_edge("block_unsafe_content", END)
agent.add_edge("process_step", END)

# Compile the agent
mission_pitch_agent = agent.compile()