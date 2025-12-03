"""RealtimeWorker - Orchestrates RealtimeListener, EventProcessor, and StateSyncService."""

import asyncio
import logging
from typing import Optional, Dict, Callable

from core.logging_config import get_logger
from core.settings import settings
from integrations.supabase.realtime_listener import RealtimeListener
from integrations.supabase.event_processor import EventProcessor, RealtimeEvent
from integrations.supabase.state_sync_service import StateSyncService

logger = get_logger(__name__)


class RealtimeWorker:
    """Orchestrates Realtime components and manages worker lifecycle."""
    
    def __init__(self):
        """Initialize RealtimeWorker."""
        self.listener: Optional[RealtimeListener] = None
        self.processor: Optional[EventProcessor] = None
        self.sync_service: Optional[StateSyncService] = None
        self.is_running: bool = False
        self.subscriptions: Dict[str, Dict] = {}  # thread_id -> subscription info
        self._task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the Realtime worker."""
        if self.is_running:
            logger.warning("RealtimeWorker: Already running")
            return
        
        if not settings.USE_SUPABASE_REALTIME:
            logger.warning(
                "RealtimeWorker: USE_SUPABASE_REALTIME is False. "
                "Worker will not start."
            )
            return
        
        try:
            # Initialize components
            self.listener = RealtimeListener()
            self.processor = EventProcessor()
            self.sync_service = StateSyncService()
            
            # Connect
            connected = await self.listener.connect()
            if not connected:
                logger.error("RealtimeWorker: Failed to connect to Supabase Realtime")
                return
            
            self.is_running = True
            logger.info("✅ RealtimeWorker: Started successfully")
            
            # Start event processing loop
            self._task = asyncio.create_task(self._process_events_loop())
        
        except Exception as e:
            logger.error(f"❌ RealtimeWorker: Failed to start: {e}", exc_info=True)
            self.is_running = False
    
    async def stop(self):
        """Stop the Realtime worker."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Cancel event processing task
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        # Unsubscribe from all channels
        if self.listener:
            await self.listener.disconnect()
        
        logger.info("✅ RealtimeWorker: Stopped")
    
    async def subscribe_to_thread(
        self,
        user_id: int,
        thread_id: str,
        agent_id: str = "founder-buddy"
    ):
        """
        Subscribe to Realtime events for a specific thread.
        
        Args:
            user_id: User ID
            thread_id: Thread ID
            agent_id: Agent ID (default: "founder-buddy")
        """
        if not self.is_running or not self.listener:
            logger.error("RealtimeWorker: Not running or listener not initialized")
            return
        
        if thread_id in self.subscriptions:
            logger.debug(f"RealtimeWorker: Already subscribed to thread {thread_id}")
            return
        
        try:
            logger.info(
                f"🔔 RealtimeWorker: Subscribing to thread {thread_id} "
                f"(user_id={user_id}, agent_id={agent_id})"
            )
            
            # Subscribe to section_states
            section_channel = await self.listener.subscribe_to_section_states(
                user_id=user_id,
                thread_id=thread_id,
                callback=self._handle_realtime_event
            )
            
            # Subscribe to business_plans
            plan_channel = await self.listener.subscribe_to_business_plans(
                user_id=user_id,
                thread_id=thread_id,
                callback=self._handle_realtime_event
            )
            
            if section_channel and plan_channel:
                self.subscriptions[thread_id] = {
                    "user_id": user_id,
                    "thread_id": thread_id,
                    "agent_id": agent_id,
                    "section_channel": section_channel,
                    "plan_channel": plan_channel,
                }
                logger.info(
                    f"✅ RealtimeWorker: Successfully subscribed to thread {thread_id} "
                    f"(user_id={user_id}, agent_id={agent_id})"
                )
                logger.info(f"   - Section channel: {section_channel}")
                logger.info(f"   - Plan channel: {plan_channel}")
            else:
                logger.error(
                    f"❌ RealtimeWorker: Failed to subscribe to thread {thread_id} "
                    f"(section_channel={section_channel}, plan_channel={plan_channel})"
                )
        
        except Exception as e:
            logger.error(
                f"❌ RealtimeWorker: Failed to subscribe to thread {thread_id}: {e}",
                exc_info=True
            )
    
    async def unsubscribe_from_thread(self, thread_id: str):
        """
        Unsubscribe from Realtime events for a specific thread.
        
        Args:
            thread_id: Thread ID
        """
        if thread_id not in self.subscriptions:
            logger.debug(f"RealtimeWorker: Not subscribed to thread {thread_id}")
            return
        
        if not self.listener:
            return
        
        try:
            subscription = self.subscriptions[thread_id]
            
            # Unsubscribe from channels
            await self.listener.unsubscribe(subscription["section_channel"])
            await self.listener.unsubscribe(subscription["plan_channel"])
            
            # Clear event queue
            if self.processor:
                await self.processor.clear_queue(thread_id)
            
            # Remove subscription
            del self.subscriptions[thread_id]
            
            logger.info(f"✅ RealtimeWorker: Unsubscribed from thread {thread_id}")
        
        except Exception as e:
            logger.error(
                f"❌ RealtimeWorker: Failed to unsubscribe from thread {thread_id}: {e}",
                exc_info=True
            )
    
    def _handle_realtime_event(self, payload: dict):
        """
        Handle Realtime event from Supabase.
        
        Args:
            payload: Raw payload from Supabase Realtime
        """
        if not self.processor:
            logger.error("RealtimeWorker: Processor not initialized")
            return
        
        try:
            logger.info(f"🔄 RealtimeWorker: Processing Realtime event - table={payload.get('table')}, type={payload.get('type')}")
            
            # Parse event
            event = self.processor.parse_payload(payload)
            if not event:
                logger.warning("⚠️ RealtimeWorker: Failed to parse event payload")
                return
            
            logger.info(f"✅ RealtimeWorker: Parsed event - {event.event_type} for thread {event.thread_id}")
            
            # Add to processing queue
            # Note: This is synchronous callback, so we use asyncio.create_task
            asyncio.create_task(self.processor.add_event(event))
        
        except Exception as e:
            logger.error(
                f"❌ RealtimeWorker: Error handling Realtime event: {e}",
                exc_info=True
            )
    
    async def _process_events_loop(self):
        """Process events from queues."""
        logger.info("RealtimeWorker: Event processing loop started")
        
        while self.is_running:
            try:
                # Process events for all subscribed threads
                for thread_id in list(self.subscriptions.keys()):
                    if not self.processor or not self.sync_service:
                        continue
                    
                    # Get next event for this thread
                    event = await self.processor.get_next_event(thread_id)
                    if not event:
                        continue
                    
                    logger.info(
                        f"🔄 RealtimeWorker: Processing event {event.event_id} "
                        f"(type: {event.event_type}) for thread {thread_id}"
                    )
                    
                    # Process event
                    success = await self.sync_service.process_event(event)
                    if success:
                        logger.info(
                            f"✅ RealtimeWorker: Successfully synced event {event.event_id} "
                            f"for thread {thread_id}"
                        )
                    else:
                        logger.warning(
                            f"⚠️ RealtimeWorker: Failed to sync event {event.event_id} "
                            f"for thread {thread_id}"
                        )
                
                # Sleep briefly to avoid busy waiting
                await asyncio.sleep(0.1)
            
            except asyncio.CancelledError:
                logger.info("RealtimeWorker: Event processing loop cancelled")
                break
            except Exception as e:
                logger.error(
                    f"❌ RealtimeWorker: Error in event processing loop: {e}",
                    exc_info=True
                )
                await asyncio.sleep(1)  # Wait before retrying
    
    async def health_check(self) -> bool:
        """
        Check worker health.
        
        Returns:
            True if healthy, False otherwise
        """
        if not self.is_running:
            return False
        
        if not self.listener:
            return False
        
        return self.listener.is_connected
    
    def get_subscription_count(self) -> int:
        """Get number of active subscriptions."""
        return len(self.subscriptions)

