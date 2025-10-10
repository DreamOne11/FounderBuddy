"""agent.py — Main entrypoint for the Concept Pitch (CAOS) Agent.
Builds and runs a LangGraph flow that generates, refines, and finalizes
three Concept Pitch variations (Pain-, Gain-, Prize-driven).
"""

import logging
import uuid
from typing import Any, Dict

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import StateGraph, MessagesState
from pydantic import BaseModel, Field

from .enums import RouterDirective, SectionID
from .graph import build_concept_pitch_graph
from .models import ContextPacket, ConceptPitchData, ConceptPitchState
from .prompts import CAOS_SYSTEM_PROMPT, PAIN_PITCH_TEMPLATE, GAIN_PITCH_TEMPLATE, PRIZE_PITCH_TEMPLATE, format_pitch_template
from .tools import get_context

logger = logging.getLogger(__name__)


# Simple AgentState model for the standalone agent functionality
class AgentState(BaseModel):
    """Simple state model for Concept Pitch agent."""
    icp: str = ""
    pain: str = ""
    gain: str = ""
    prize: str = ""
    signature_method: str = ""
    concept_pitch: Dict[str, Any] = Field(default_factory=dict)
    needs_refinement: bool = False
    checklist_ready: bool = False
    messages: list[BaseMessage] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Response model for Concept Pitch agent."""
    success: bool = True
    message: str = ""
    concept_pitch: Dict[str, Any] = Field(default_factory=dict)


def get_concept_pitch_prompt() -> str:
    """Get the CAOS system prompt for concept pitch generation."""
    return CAOS_SYSTEM_PROMPT


def generate_concept_pitch(state: AgentState) -> AgentState:
    """Generate three concept pitch variations based on user input."""
    logger.info("Generating concept pitch variations")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    system_prompt = get_concept_pitch_prompt()
    
    user_input = (
        f"ICP: {state.icp}\n"
        f"Pain: {state.pain}\n"
        f"Gain: {state.gain}\n"
        f"Prize: {state.prize}\n"
        f"Signature Method: {state.signature_method}\n"
    )
    
    full_prompt = system_prompt + "\n" + user_input
    
    try:
        response = llm.invoke(full_prompt)
        
        # Format the three pitch templates with user data
        pitch_data = {
            "ICP": state.icp,
            "Pain": state.pain,
            "Pain_Consequence": f"struggling with {state.pain}",
            "Solution_Type": "solution",
            "Gain": state.gain,
            "Objection": "complex processes",
            "Timeframe": "a few weeks",
            "Prize": state.prize,
        }
        
        state.concept_pitch = {
            "pain_pitch": format_pitch_template("pain", pitch_data),
            "gain_pitch": format_pitch_template("gain", pitch_data),
            "prize_pitch": format_pitch_template("prize", pitch_data),
            "llm_response": response.content,
            "raw_data": pitch_data
        }
        state.needs_refinement = True
        
        logger.info("Successfully generated concept pitch variations")
        
    except Exception as e:
        logger.error(f"Error generating concept pitch: {e}")
        state.concept_pitch = {
            "error": str(e),
            "pain_pitch": "Error generating pitch",
            "gain_pitch": "Error generating pitch", 
            "prize_pitch": "Error generating pitch"
        }
        state.needs_refinement = False
    
    return state


def refinement_node(state: AgentState) -> AgentState:
    """Handle pitch refinement based on user feedback."""
    logger.info("Processing pitch refinement")
    
    if state.needs_refinement:
        # Import refine function (placeholder implementation)
        try:
            from .refine import refine_pitch
            state = refine_pitch(state)
        except ImportError:
            logger.warning("Refine module not available, skipping refinement")
            state.needs_refinement = False
            state.checklist_ready = True
    else:
        state.checklist_ready = True
    
    logger.info(f"Refinement complete. Ready: {state.checklist_ready}")
    return state


def save_node(state: AgentState) -> AgentState:
    """Save the final confirmed pitch to project."""
    logger.info("Saving concept pitch to project")
    
    try:
        from .sync import save_pitch_to_project
        save_pitch_to_project("concept_pitch", state.concept_pitch)
        logger.info("Successfully saved concept pitch")
    except ImportError:
        logger.warning("Sync module not available, skipping save")
    except Exception as e:
        logger.error(f"Error saving concept pitch: {e}")
    
    return state


def build_simple_concept_pitch_graph() -> StateGraph:
    """Build the LangGraph state machine for concept pitch generation."""
    logger.info("Building concept pitch graph")
    
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("generate", generate_concept_pitch)
    graph.add_node("refine", refinement_node)
    graph.add_node("save", save_node)
    
    # Add edges
    graph.add_edge(START, "generate")
    
    # Conditional edge from generate to refine or save
    graph.add_conditional_edges(
        "generate",
        lambda s: "refine" if s.needs_refinement else "save",
        {"refine": "refine", "save": "save"}
    )
    
    graph.add_edge("refine", "save")
    graph.add_edge("save", END)
    
    logger.info("Concept pitch graph built successfully")
    return graph


def run_concept_pitch_agent(initial_state: AgentState) -> AgentState:
    """Run the concept pitch agent with the given initial state."""
    logger.info("Starting concept pitch agent")
    
    try:
        graph = build_simple_concept_pitch_graph().compile()
        result = graph.run(initial_state)
        logger.info("Concept pitch agent completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error running concept pitch agent: {e}")
        initial_state.concept_pitch = {"error": str(e)}
        return initial_state


# # Create the runnable graph for the main agent system
# graph = build_concept_pitch_graph()


# # Initialize function for new conversations (for compatibility with existing system)
# async def initialize_concept_pitch_state(user_id: int = None, thread_id: str = None) -> ConceptPitchState:
#     """Initialize a new Concept Pitch state.
    
#     Args:
#         user_id: Integer user ID from frontend (will use default if not provided)
#         thread_id: Thread UUID (will be generated if not provided)
#     """
    
#     # Use provided integer user_id or default to 1
#     if not user_id:
#         user_id = 1
#         logger.info(f"Using default user_id: {user_id}")
#     else:
#         logger.info(f"Using provided user_id: {user_id}")

#     # Ensure thread_id is a valid UUID string
#     if not thread_id:
#         thread_id = str(uuid.uuid4())
#         logger.info(f"Generated new thread_id: {thread_id}")
#     else:
#         try:
#             uuid.UUID(thread_id)
#         except ValueError:
#             thread_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, thread_id))
#             logger.info(f"Converted non-UUID thread_id to UUID: {thread_id}")
    
#     initial_state = ConceptPitchState(
#         user_id=user_id,
#         thread_id=thread_id,
#         messages=[],
#         current_section=SectionID.SUMMARY_CONFIRMATION,
#         router_directive=RouterDirective.NEXT,  # Start by loading first section
#     )
    
#     # Get initial context
#     context = await get_context.ainvoke({
#         "user_id": user_id,
#         "thread_id": thread_id,
#         "section_id": SectionID.SUMMARY_CONFIRMATION.value,
#         "canvas_data": {},
#     })
    
#     initial_state["context_packet"] = ContextPacket(**context)
    
#     return initial_state


# # Test function for standalone usage
# if __name__ == "__main__":
#     # Test the agent with sample data
#     state = AgentState(
#         icp="startup founders", 
#         pain="burnout and lack of clarity", 
#         gain="strategic clarity and sustainable growth", 
#         prize="freedom to build what matters", 
#         signature_method="CAOS framework"
#     )
    
#     print("🚀 Testing Concept Pitch Agent...")
#     print(f"Input: ICP={state.icp}, Pain={state.pain}")
    
#     result = run_concept_pitch_agent(state)
    
#     print("\n📋 Generated Concept Pitches:")
#     print("=" * 50)
    
#     if "error" in result.concept_pitch:
#         print(f"❌ Error: {result.concept_pitch['error']}")
#     else:
#         print("🎯 Pain-Driven Pitch:")
#         print(result.concept_pitch.get("pain_pitch", "Not generated"))
#         print("\n🎯 Gain-Driven Pitch:")
#         print(result.concept_pitch.get("gain_pitch", "Not generated"))
#         print("\n🎯 Prize-Driven Pitch:")
#         print(result.concept_pitch.get("prize_pitch", "Not generated"))
    
#     print(f"\n✅ Agent completed. Needs refinement: {result.needs_refinement}")


# __all__ = [
#     "graph", 
#     "initialize_concept_pitch_state", 
#     "run_concept_pitch_agent",
#     "AgentState",
#     "AgentResponse",
#     "generate_concept_pitch",
#     "refinement_node", 
#     "save_node",
#     "build_concept_pitch_graph"
# ]
# Create the runnable graph for the main agent system
# ✅ build_concept_pitch_graph() 已经返回编译后的图
graph = build_concept_pitch_graph()

# Initialize function for new conversations (for compatibility with existing system)
async def initialize_concept_pitch_state(user_id: int = None, thread_id: str = None) -> ConceptPitchState:
    """Initialize a new Concept Pitch state.
    
    Args:
        user_id: Integer user ID from frontend (will use default if not provided)
        thread_id: Thread UUID (will be generated if not provided)
    """
    
    # Use provided integer user_id or default to 1
    if not user_id:
        user_id = 1
        logger.info(f"Using default user_id: {user_id}")
    else:
        logger.info(f"Using provided user_id: {user_id}")

    # Ensure thread_id is a valid UUID string
    if not thread_id:
        thread_id = str(uuid.uuid4())
        logger.info(f"Generated new thread_id: {thread_id}")
    else:
        try:
            uuid.UUID(thread_id)
        except ValueError:
            thread_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, thread_id))
            logger.info(f"Converted non-UUID thread_id to UUID: {thread_id}")
    
    initial_state = ConceptPitchState(
        user_id=user_id,
        thread_id=thread_id,
        messages=[],
        current_section=SectionID.SUMMARY_CONFIRMATION,
        router_directive=RouterDirective.NEXT,  # Start by loading first section
    )
    
    # Get initial context with Value Canvas data
    context = await get_context.ainvoke({
        "user_id": user_id,
        "thread_id": thread_id,
        "section_id": SectionID.SUMMARY_CONFIRMATION.value,
        "canvas_data": {},
    })
    
    initial_state["context_packet"] = ContextPacket(**context)
    
    # Extract Value Canvas data for Concept Pitch generation
    value_canvas_data = context.get("value_canvas_data", {})
    if value_canvas_data:
        logger.info(f"CONCEPT_PITCH_INIT: ✅ Retrieved Value Canvas data: {list(value_canvas_data.keys())}")
        
        # Create ConceptPitchData and map Value Canvas data to it
        canvas_data = ConceptPitchData()
        
        if value_canvas_data.get("icp"):
            canvas_data.icp_summary = value_canvas_data["icp"]
            logger.info(f"CONCEPT_PITCH_INIT: ✅ Set ICP summary from Value Canvas")
        
        if value_canvas_data.get("pain"):
            canvas_data.pain_summary = value_canvas_data["pain"]
            logger.info(f"CONCEPT_PITCH_INIT: ✅ Set Pain summary from Value Canvas")
        
        if value_canvas_data.get("payoffs"):
            canvas_data.gain_summary = value_canvas_data["payoffs"]
            logger.info(f"CONCEPT_PITCH_INIT: ✅ Set Gain summary from Value Canvas Payoffs")
        
        if value_canvas_data.get("prize"):
            canvas_data.prize_summary = value_canvas_data["prize"]
            logger.info(f"CONCEPT_PITCH_INIT: ✅ Set Prize summary from Value Canvas")
        
        # Update the canvas_data in the state (initial_state is a dict, not a Pydantic model)
        initial_state["canvas_data"] = canvas_data
        
        logger.info(f"CONCEPT_PITCH_INIT: ✅ Concept Pitch state initialized with Value Canvas data")
    else:
        logger.warning("CONCEPT_PITCH_INIT: ⚠️ No Value Canvas data available, using empty state")
        # Still set empty canvas_data to avoid KeyError
        initial_state["canvas_data"] = ConceptPitchData()
    
    return initial_state


# Test function for standalone usage
if __name__ == "__main__":
    # Test the agent with sample data
    state = AgentState(
        icp="startup founders", 
        pain="burnout and lack of clarity", 
        gain="strategic clarity and sustainable growth", 
        prize="freedom to build what matters", 
        signature_method="CAOS framework"
    )
    
    print("🚀 Testing Concept Pitch Agent...")
    print(f"Input: ICP={state.icp}, Pain={state.pain}")
    
    result = run_concept_pitch_agent(state)
    
    print("\n📋 Generated Concept Pitches:")
    print("=" * 50)
    
    if "error" in result.concept_pitch:
        print(f"❌ Error: {result.concept_pitch['error']}")
    else:
        print("🎯 Pain-Driven Pitch:")
        print(result.concept_pitch.get("pain_pitch", "Not generated"))
        print("\n🎯 Gain-Driven Pitch:")
        print(result.concept_pitch.get("gain_pitch", "Not generated"))
        print("\n🎯 Prize-Driven Pitch:")
        print(result.concept_pitch.get("prize_pitch", "Not generated"))
    
    print(f"\n✅ Agent completed. Needs refinement: {result.needs_refinement}")


__all__ = [
    "graph", 
    "initialize_concept_pitch_state", 
    "run_concept_pitch_agent",
    "AgentState",
    "AgentResponse",
    "generate_concept_pitch",
    "refinement_node", 
    "save_node",
    "build_concept_pitch_graph"
]
