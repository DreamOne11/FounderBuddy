#!/usr/bin/env python3
"""Debug Concept Pitch agent initialization and flow."""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def debug_concept_pitch_flow():
    """Debug the complete Concept Pitch flow."""
    try:
        from src.agents.concept_pitch.agent import initialize_concept_pitch_state
        from src.agents.concept_pitch.enums import SectionID
        
        logger.info("=== DEBUGGING CONCEPT PITCH FLOW ===")
        
        # Test initialization
        user_id = 1
        thread_id = "debug-thread-001"
        
        logger.info(f"Initializing state for user_id={user_id}, thread_id={thread_id}")
        state = await initialize_concept_pitch_state(user_id=user_id, thread_id=thread_id)
        
        logger.info("=== INITIAL STATE ===")
        logger.info(f"Current section: {state.get('current_section')}")
        logger.info(f"Router directive: {state.get('router_directive')}")
        logger.info(f"Messages count: {len(state.get('messages', []))}")
        
        # Check context packet
        context_packet = state.get('context_packet')
        if context_packet:
            logger.info(f"Context packet section_id: {context_packet.section_id}")
            logger.info(f"Context packet status: {context_packet.status}")
            logger.info(f"System prompt length: {len(context_packet.system_prompt) if context_packet.system_prompt else 0}")
        
        # Check canvas data
        canvas_data = state.get('canvas_data')
        if canvas_data:
            logger.info("=== CANVAS DATA ===")
            logger.info(f"ICP: {getattr(canvas_data, 'icp_summary', 'None')[:100]}...")
            logger.info(f"Pain: {getattr(canvas_data, 'pain_summary', 'None')[:100]}...")
            logger.info(f"Gain: {getattr(canvas_data, 'gain_summary', 'None')[:100]}...")
            logger.info(f"Prize: {getattr(canvas_data, 'prize_summary', 'None')[:100]}...")
        else:
            logger.warning("No canvas data found!")
            
    except Exception as e:
        logger.error(f"Error debugging Concept Pitch flow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_concept_pitch_flow())

