"""Implementation node for Value Canvas Agent."""

import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from ..models import ValueCanvasState
from ..tools import export_checklist

logger = logging.getLogger(__name__)

# Implementation tools
implementation_tools = [
    export_checklist,
]

# Create tool node
implementation_tool_node = ToolNode(implementation_tools)


async def implementation_node(state: ValueCanvasState, config: RunnableConfig) -> ValueCanvasState:
    """
    Implementation node that generates the final checklist/PDF.
    
    Only runs when all sections are complete.
    """
    logger.info("Implementation node - Generating final deliverables")
    
    try:
        # Export checklist
        result = await export_checklist.ainvoke({
            "user_id": state["user_id"],
            "thread_id": state["thread_id"],
            "canvas_data": state["canvas_data"].model_dump(),
        })
        
        # Add completion message
        completion_msg = AIMessage(
            content=f"Congratulations! Your Value Canvas is complete. "
            f"You can download your implementation checklist here: {result['url']}"
        )
        state["messages"].append(completion_msg)
        
    except Exception as e:
        logger.error(f"Error generating implementation: {e}")
        error_msg = AIMessage(
            content=f"I encountered an error generating your checklist: {str(e)}. "
            "Your Value Canvas data has been saved and you can try exporting again later."
        )
        state["messages"].append(error_msg)
    
    return state