"""EventProcessor - Parses, validates, deduplicates, and orders Realtime events."""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict

from core.logging_config import get_logger

logger = get_logger(__name__)


class RealtimeEventType(str, Enum):
    """Types of Realtime events."""
    SECTION_STATE_UPDATED = "section_state_updated"
    SECTION_STATE_INSERTED = "section_state_inserted"
    SECTION_STATE_DELETED = "section_state_deleted"
    BUSINESS_PLAN_UPDATED = "business_plan_updated"
    BUSINESS_PLAN_INSERTED = "business_plan_inserted"
    BUSINESS_PLAN_DELETED = "business_plan_deleted"


@dataclass
class RealtimeEvent:
    """Structured Realtime event."""
    event_type: RealtimeEventType
    user_id: int
    thread_id: str
    section_id: Optional[str] = None  # For section events
    payload: dict = field(default_factory=dict)  # Event-specific data
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: str = ""  # For deduplication
    table: str = ""
    operation: str = ""  # INSERT, UPDATE, DELETE
    
    def __post_init__(self):
        """Generate event_id if not provided."""
        if not self.event_id:
            self.event_id = self._generate_event_id()
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID for deduplication."""
        return f"{self.table}:{self.thread_id}:{self.section_id or 'none'}:{self.timestamp.isoformat()}"


class EventProcessor:
    """Processes Realtime events: parsing, validation, deduplication, ordering."""
    
    def __init__(self, cache_ttl_seconds: int = 3600):
        """
        Initialize EventProcessor.
        
        Args:
            cache_ttl_seconds: Time to keep processed events in cache (default: 1 hour)
        """
        self.processed_events: set[str] = set()
        self.cache_ttl_seconds = cache_ttl_seconds
        self.event_queues: dict[str, list[RealtimeEvent]] = defaultdict(list)  # thread_id -> events
        self.locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
    
    def parse_payload(self, payload: dict) -> Optional[RealtimeEvent]:
        """
        Parse Realtime payload into RealtimeEvent.
        
        Args:
            payload: Raw payload from Supabase Realtime
        
        Returns:
            Parsed RealtimeEvent or None if parsing fails
        """
        try:
            # Log full payload for debugging
            logger.debug(f"📦 EventProcessor: Parsing payload - keys: {list(payload.keys())}")
            logger.debug(f"📦 EventProcessor: Full payload: {payload}")
            
            # Extract event information
            # realtime-py may send data in different formats
            # Try multiple possible field names
            event_type_str = (
                payload.get("eventType") or 
                payload.get("event_type") or 
                payload.get("event") or
                ""
            )
            
            table = (
                payload.get("table") or 
                payload.get("table_name") or
                ""
            )
            
            operation = (
                payload.get("type") or 
                payload.get("eventType") or 
                event_type_str or
                ""
            ).upper()
            
            # If operation is still empty, try to infer from eventType
            if not operation and event_type_str:
                operation = event_type_str.upper()
            
            logger.info(f"📦 EventProcessor: Extracted - table={table}, operation={operation}, eventType={event_type_str}")
            logger.debug(f"📦 EventProcessor: Full payload keys: {list(payload.keys())}")
            
            # Extract new/old data
            # Try multiple possible field names
            new_data = payload.get("new") or payload.get("new_record") or payload.get("record") or {}
            old_data = payload.get("old") or payload.get("old_record") or {}
            
            # If new_data is not a dict, try to extract from nested structure
            if not isinstance(new_data, dict):
                logger.warning(f"⚠️ EventProcessor: new_data is not a dict: {type(new_data)}")
                new_data = {}
            
            if not isinstance(old_data, dict):
                old_data = {}
            
            logger.debug(f"📦 EventProcessor: new_data keys: {list(new_data.keys()) if isinstance(new_data, dict) else 'Not a dict'}")
            
            # If table is still empty, try to infer from new_data or old_data
            if not table:
                # Try to get table name from metadata or other fields
                table = (
                    payload.get("schema") or
                    payload.get("table_name") or
                    ""
                )
                logger.warning(f"⚠️ EventProcessor: Table name not found in payload, trying alternatives: {table}")
            
            # Determine event type
            if table == "section_states":
                if operation == "INSERT":
                    event_type = RealtimeEventType.SECTION_STATE_INSERTED
                elif operation == "UPDATE":
                    event_type = RealtimeEventType.SECTION_STATE_UPDATED
                elif operation == "DELETE":
                    event_type = RealtimeEventType.SECTION_STATE_DELETED
                else:
                    logger.warning(f"Unknown operation: {operation}")
                    return None
                
                # Extract IDs
                user_id = new_data.get("user_id") or old_data.get("user_id")
                thread_id = new_data.get("thread_id") or old_data.get("thread_id")
                section_id = new_data.get("section_id") or old_data.get("section_id")
                
                if not user_id or not thread_id:
                    logger.warning("Missing user_id or thread_id in payload")
                    return None
                
                # Extract timestamp
                updated_at_str = new_data.get("updated_at") or old_data.get("updated_at")
                timestamp = datetime.now()
                if updated_at_str:
                    try:
                        timestamp = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                    except Exception:
                        pass  # Use current time if parsing fails
                
                return RealtimeEvent(
                    event_type=event_type,
                    user_id=int(user_id),
                    thread_id=str(thread_id),
                    section_id=str(section_id) if section_id else None,
                    payload={
                        "new": new_data,
                        "old": old_data,
                    },
                    timestamp=timestamp,
                    table=table,
                    operation=operation,
                )
            
            elif table == "business_plans":
                if operation == "INSERT":
                    event_type = RealtimeEventType.BUSINESS_PLAN_INSERTED
                elif operation == "UPDATE":
                    event_type = RealtimeEventType.BUSINESS_PLAN_UPDATED
                elif operation == "DELETE":
                    event_type = RealtimeEventType.BUSINESS_PLAN_DELETED
                else:
                    logger.warning(f"Unknown operation: {operation}")
                    return None
                
                # Extract IDs
                user_id = new_data.get("user_id") or old_data.get("user_id")
                thread_id = new_data.get("thread_id") or old_data.get("thread_id")
                
                if not user_id or not thread_id:
                    logger.warning("Missing user_id or thread_id in payload")
                    return None
                
                # Extract timestamp
                updated_at_str = new_data.get("updated_at") or old_data.get("updated_at")
                timestamp = datetime.now()
                if updated_at_str:
                    try:
                        timestamp = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                    except Exception:
                        pass
                
                return RealtimeEvent(
                    event_type=event_type,
                    user_id=int(user_id),
                    thread_id=str(thread_id),
                    payload={
                        "new": new_data,
                        "old": old_data,
                    },
                    timestamp=timestamp,
                    table=table,
                    operation=operation,
                )
            
            else:
                logger.warning(f"Unknown table: {table}")
                return None
        
        except Exception as e:
            logger.error(f"❌ EventProcessor: Failed to parse payload: {e}", exc_info=True)
            return None
    
    def validate_event(self, event: RealtimeEvent) -> bool:
        """
        Validate event data.
        
        Args:
            event: Event to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not event.user_id or not event.thread_id:
            logger.warning("Event missing required fields: user_id or thread_id")
            return False
        
        if event.event_type in [
            RealtimeEventType.SECTION_STATE_UPDATED,
            RealtimeEventType.SECTION_STATE_INSERTED,
            RealtimeEventType.SECTION_STATE_DELETED,
        ]:
            if not event.section_id:
                logger.warning("Section event missing section_id")
                return False
        
        return True
    
    def is_duplicate(self, event: RealtimeEvent) -> bool:
        """
        Check if event is duplicate.
        
        Args:
            event: Event to check
        
        Returns:
            True if duplicate, False otherwise
        """
        if event.event_id in self.processed_events:
            logger.debug(f"Duplicate event detected: {event.event_id}")
            return True
        
        # Add to processed events
        self.processed_events.add(event.event_id)
        return False
    
    def order_events(self, thread_id: str) -> list[RealtimeEvent]:
        """
        Get ordered events for a thread.
        
        Args:
            thread_id: Thread ID
        
        Returns:
            List of events ordered by timestamp
        """
        if thread_id not in self.event_queues:
            return []
        
        # Sort by timestamp
        events = sorted(self.event_queues[thread_id], key=lambda e: e.timestamp)
        return events
    
    async def add_event(self, event: RealtimeEvent) -> bool:
        """
        Add event to processing queue.
        
        Args:
            event: Event to add
        
        Returns:
            True if added, False if duplicate or invalid
        """
        # Validate
        if not self.validate_event(event):
            logger.warning(f"⚠️ EventProcessor: Event validation failed for {event.event_id}")
            return False
        
        # Check duplicate
        if self.is_duplicate(event):
            logger.debug(f"⚠️ EventProcessor: Duplicate event detected: {event.event_id}")
            return False
        
        # Add to queue
        thread_id = event.thread_id
        async with self.locks[thread_id]:
            self.event_queues[thread_id].append(event)
            # Sort by timestamp
            self.event_queues[thread_id].sort(key=lambda e: e.timestamp)
        
        logger.info(f"📥 EventProcessor: Added event {event.event_id} to queue for thread {thread_id} (type: {event.event_type})")
        return True
    
    async def get_next_event(self, thread_id: str) -> Optional[RealtimeEvent]:
        """
        Get next event from queue for a thread.
        
        Args:
            thread_id: Thread ID
        
        Returns:
            Next event or None if queue is empty
        """
        async with self.locks[thread_id]:
            if not self.event_queues[thread_id]:
                return None
            
            return self.event_queues[thread_id].pop(0)
    
    async def clear_queue(self, thread_id: str):
        """Clear event queue for a thread."""
        if thread_id in self.event_queues:
            async with self.locks[thread_id]:
                self.event_queues[thread_id].clear()

