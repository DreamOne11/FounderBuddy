"""Implementation node for Signature Pitch Agent."""

import logging

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

from ..models import SignaturePitchState
from ..tools import export_signature_pitch_framework

logger = logging.getLogger(__name__)


async def implementation_node(
    state: SignaturePitchState, config: RunnableConfig
) -> SignaturePitchState:
    """
    Implementation node that generates final signature pitch framework exports.
    """
    logger.info("Implementation node - Generating signature pitch framework")

    try:
        # Generate signature pitch framework export
        framework_content = await export_signature_pitch_framework.ainvoke(
            {
                "user_id": state["user_id"],
                "thread_id": state["thread_id"],
                "canvas_data": state["canvas_data"],
            }
        )

        # Create implementation response
        response_content = (
            f"Your complete Signature Pitch Framework has been generated:\\n\\n{framework_content}"
        )

        state["messages"].append(AIMessage(content=response_content))
        state["finished"] = True

        logger.info("Implementation node - Successfully generated signature pitch framework")

    except Exception as e:
        logger.error(f"Implementation node - Error generating framework: {e}")
        fallback_response = "I apologize, but there was an error generating your signature pitch framework. Please try again."
        state["messages"].append(AIMessage(content=fallback_response))
        state["error_count"] = state.get("error_count", 0) + 1
        state["last_error"] = str(e)

    return state
