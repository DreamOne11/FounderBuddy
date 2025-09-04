"""Implementation node for Mission Pitch Agent."""

import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

from ..models import MissionPitchState
from ..tools import export_mission_framework

logger = logging.getLogger(__name__)


async def implementation_node(state: MissionPitchState, config: RunnableConfig) -> MissionPitchState:
    """
    Implementation node that generates final mission framework exports.
    """
    logger.info("Implementation node - Generating mission framework")
    
    try:
        # Generate mission framework export
        framework_content = await export_mission_framework.ainvoke({
            "user_id": state["user_id"],
            "thread_id": state["thread_id"],
            "canvas_data": state["canvas_data"].model_dump(),
        })
        
        # Create implementation response
        response_content = f"Your complete Mission Framework has been generated:\\n\\n{framework_content}"
        
        state["messages"].append(AIMessage(content=response_content))
        state["finished"] = True
        
        logger.info("Implementation node - Successfully generated mission framework")
        
    except Exception as e:
        logger.error(f"Implementation node - Error generating framework: {e}")
        fallback_response = "I apologize, but there was an error generating your mission framework. Please try again."
        state["messages"].append(AIMessage(content=fallback_response))
        state["error_count"] = state.get("error_count", 0) + 1
        state["last_error"] = str(e)
    
    return state
