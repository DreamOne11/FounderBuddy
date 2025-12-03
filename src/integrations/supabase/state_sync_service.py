"""StateSyncService - Synchronizes Supabase changes with LangGraph agent state."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from typing import Union

from core.logging_config import get_logger
from core.settings import settings
from memory.postgres import pg_manager
from memory.sqlite import get_sqlite_saver
from agents import get_agent, AgentGraph
from integrations.supabase.event_processor import RealtimeEvent, RealtimeEventType

logger = get_logger(__name__)


class StateSyncService:
    """Synchronizes database changes with LangGraph agent state."""
    
    def __init__(self):
        """Initialize StateSyncService."""
        self.checkpoint_store: Optional[Union[AsyncPostgresSaver, AsyncSqliteSaver]] = None
        self._init_checkpoint_store()
    
    def _init_checkpoint_store(self):
        """Initialize checkpoint store from pg_manager or sqlite."""
        try:
            if settings.DATABASE_TYPE.value == "postgres":
                self.checkpoint_store = pg_manager.get_saver()
                logger.info("✅ StateSyncService: Checkpoint store initialized (PostgreSQL)")
            elif settings.DATABASE_TYPE.value == "sqlite":
                # SQLite saver is a context manager, we need to handle it differently
                # For now, we'll get it from the agent's checkpointer
                logger.info("✅ StateSyncService: Using SQLite checkpoint store (will get from agent)")
            else:
                logger.warning(
                    "StateSyncService: Checkpoint store only available with PostgreSQL or SQLite. "
                    f"Current database type: {settings.DATABASE_TYPE}"
                )
        except Exception as e:
            logger.error(f"❌ StateSyncService: Failed to initialize checkpoint store: {e}")
    
    async def sync_section_state(
        self,
        agent_id: str,
        thread_id: str,
        user_id: int,
        section_id: str,
        new_content: dict,
        new_status: Optional[str] = None,
        new_satisfaction_status: Optional[str] = None
    ) -> bool:
        """
        Sync section state update to LangGraph agent state.
        
        Args:
            agent_id: Agent ID (e.g., "founder-buddy")
            thread_id: Thread ID
            user_id: User ID
            section_id: Section ID
            new_content: New Tiptap JSON content
            new_status: New status (optional)
            new_satisfaction_status: New satisfaction status (optional)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get agent
            agent: AgentGraph = get_agent(agent_id)
            
            # Get current state
            config = RunnableConfig(
                configurable={
                    "thread_id": thread_id,
                    "user_id": user_id
                }
            )
            
            state_snapshot = await agent.aget_state(config)
            if not state_snapshot or not state_snapshot.values:
                logger.warning(f"StateSyncService: No state found for thread {thread_id}")
                return False
            
            current_state = state_snapshot.values
            
            # Update section_states
            if "section_states" not in current_state:
                current_state["section_states"] = {}
            
            # Import section models
            from agents.founder_buddy.models import SectionState, SectionContent, SectionStatus
            from agents.founder_buddy.enums import SectionID
            
            # Convert Tiptap JSON to SectionContent
            section_content = SectionContent(
                content=new_content,  # Tiptap JSON
                plain_text=self._extract_plain_text(new_content)
            )
            
            # Determine status
            if new_status:
                try:
                    status = SectionStatus(new_status)
                except ValueError:
                    status = SectionStatus.IN_PROGRESS
            else:
                # Try to get existing status
                existing_section = current_state["section_states"].get(section_id)
                if existing_section:
                    status = existing_section.get("status", SectionStatus.IN_PROGRESS)
                else:
                    status = SectionStatus.IN_PROGRESS
            
            # Create or update SectionState
            try:
                section_id_enum = SectionID(section_id)
            except ValueError:
                logger.warning(f"StateSyncService: Invalid section_id: {section_id}")
                return False
            
            section_state = SectionState(
                section_id=section_id_enum,
                content=section_content,
                status=status,
                satisfaction_status=new_satisfaction_status
            )
            
            # Update state
            current_state["section_states"][section_id] = section_state.model_dump()
            
            # Save updated state to checkpoint store
            # Note: LangGraph doesn't have direct update_state API
            # We need to use a workaround - create a checkpoint with updated state
            await self._update_checkpoint_state(agent, config, current_state)
            
            logger.info(
                f"✅ StateSyncService: Synced section_state for "
                f"thread={thread_id}, section={section_id}"
            )
            
            return True
        
        except Exception as e:
            logger.error(
                f"❌ StateSyncService: Failed to sync section_state: {e}",
                exc_info=True
            )
            return False
    
    async def sync_business_plan(
        self,
        agent_id: str,
        thread_id: str,
        user_id: int,
        new_content: str
    ) -> bool:
        """
        Sync business plan update to LangGraph agent state.
        
        Args:
            agent_id: Agent ID (e.g., "founder-buddy")
            thread_id: Thread ID
            user_id: User ID
            new_content: New business plan content (markdown)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get agent
            agent: AgentGraph = get_agent(agent_id)
            
            # Get current state
            config = RunnableConfig(
                configurable={
                    "thread_id": thread_id,
                    "user_id": user_id
                }
            )
            
            state_snapshot = await agent.aget_state(config)
            if not state_snapshot or not state_snapshot.values:
                logger.warning(f"StateSyncService: No state found for thread {thread_id}")
                return False
            
            current_state = state_snapshot.values
            
            # Update business_plan
            current_state["business_plan"] = new_content
            
            # Save updated state to checkpoint store
            await self._update_checkpoint_state(agent, config, current_state)
            
            logger.info(
                f"✅ StateSyncService: Synced business_plan for thread={thread_id}"
            )
            
            return True
        
        except Exception as e:
            logger.error(
                f"❌ StateSyncService: Failed to sync business_plan: {e}",
                exc_info=True
            )
            return False
    
    async def _update_checkpoint_state(
        self,
        agent: AgentGraph,
        config: RunnableConfig,
        updated_state: Dict[str, Any]
    ):
        """
        Update checkpoint state directly.
        
        Note: This is a workaround since LangGraph doesn't have direct update_state API.
        We create a new checkpoint with the updated state.
        """
        # Get checkpoint store from agent's checkpointer
        checkpoint_store = None
        if hasattr(agent, 'checkpointer') and agent.checkpointer:
            checkpoint_store = agent.checkpointer
        elif self.checkpoint_store:
            checkpoint_store = self.checkpoint_store
        
        if not checkpoint_store:
            logger.warning(
                "StateSyncService: Checkpoint store not available. "
                "State will be updated in memory but may not persist. "
                "Consider using PostgreSQL for full Realtime sync support."
            )
            # Still return True to allow the sync to continue
            # The state will be updated when Agent next loads it from Supabase
            return
        
        try:
            # Get current checkpoint
            checkpoint = await checkpoint_store.get(config)
            
            if checkpoint:
                # Update checkpoint with new state
                checkpoint["channel_values"] = updated_state
                checkpoint["channel_versions"] = {
                    k: checkpoint.get("channel_versions", {}).get(k, 0) + 1
                    for k in updated_state.keys()
                }
                
                # Save updated checkpoint
                await checkpoint_store.put(config, checkpoint)
                logger.debug(f"✅ StateSyncService: Updated checkpoint for thread {config.configurable.get('thread_id')}")
            else:
                # Create new checkpoint
                checkpoint = {
                    "channel_values": updated_state,
                    "channel_versions": {k: 1 for k in updated_state.keys()},
                    "versions_seen": {},
                }
                await checkpoint_store.put(config, checkpoint)
                logger.debug(f"✅ StateSyncService: Created new checkpoint for thread {config.configurable.get('thread_id')}")
        
        except Exception as e:
            logger.error(
                f"StateSyncService: Failed to update checkpoint state: {e}",
                exc_info=True
            )
            # Don't raise - allow sync to continue even if checkpoint update fails
            logger.warning("StateSyncService: Continuing without checkpoint update")
    
    def _extract_plain_text(self, tiptap_json: dict) -> str:
        """
        Extract plain text from Tiptap JSON.
        
        Args:
            tiptap_json: Tiptap JSON structure
        
        Returns:
            Plain text content
        """
        def extract_text(node: dict) -> str:
            if node.get("type") == "text":
                return node.get("text", "")
            elif node.get("type") == "paragraph":
                if "content" in node:
                    return " ".join(extract_text(child) for child in node["content"])
                return ""
            elif "content" in node:
                return " ".join(extract_text(child) for child in node["content"])
            return ""
        
        if not tiptap_json:
            return ""
        
        content = tiptap_json.get("content", [])
        if not content:
            return ""
        
        return " ".join(extract_text(node) for node in content).strip()
    
    async def process_event(self, event: RealtimeEvent) -> bool:
        """
        Process a Realtime event and sync state.
        
        Args:
            event: Realtime event to process
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(
                f"🔄 StateSyncService: Processing event {event.event_id} "
                f"(type: {event.event_type}, thread: {event.thread_id})"
            )
            
            # Determine agent_id from event
            # For now, assume founder-buddy
            agent_id = "founder-buddy"
            
            if event.event_type in [
                RealtimeEventType.SECTION_STATE_UPDATED,
                RealtimeEventType.SECTION_STATE_INSERTED,
            ]:
                logger.info(f"📝 StateSyncService: Syncing section_state for section {event.section_id}")
                new_data = event.payload.get("new", {})
                content = new_data.get("content")
                status = new_data.get("status")
                satisfaction_status = new_data.get("satisfaction_status")
                
                if not content:
                    logger.warning("StateSyncService: No content in event payload")
                    return False
                
                return await self.sync_section_state(
                    agent_id=agent_id,
                    thread_id=event.thread_id,
                    user_id=event.user_id,
                    section_id=event.section_id or "",
                    new_content=content,
                    new_status=status,
                    new_satisfaction_status=satisfaction_status
                )
            
            elif event.event_type == RealtimeEventType.BUSINESS_PLAN_UPDATED:
                logger.info(f"📄 StateSyncService: Syncing business_plan")
                new_data = event.payload.get("new", {})
                content = new_data.get("content") or new_data.get("markdown_content")
                
                if not content:
                    logger.warning("StateSyncService: No content in business plan event")
                    return False
                
                return await self.sync_business_plan(
                    agent_id=agent_id,
                    thread_id=event.thread_id,
                    user_id=event.user_id,
                    new_content=content
                )
            
            else:
                logger.debug(f"StateSyncService: Ignoring event type: {event.event_type}")
                return True  # Not an error, just not handled
        
        except Exception as e:
            logger.error(
                f"❌ StateSyncService: Failed to process event: {e}",
                exc_info=True
            )
            return False

