"""RealtimeListener - Manages Supabase Realtime WebSocket connections."""

import asyncio
import logging
from typing import Callable, Optional
from datetime import datetime

from core.settings import settings
from core.logging_config import get_logger

logger = get_logger(__name__)

# Try to import realtime-py library
try:
    from realtime import AsyncRealtimeClient
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False
    logger.warning("realtime-py library not installed. Install with: pip install realtime")


class RealtimeListener:
    """Manages Supabase Realtime WebSocket connections and subscriptions."""
    
    def __init__(self):
        """Initialize RealtimeListener with Supabase Realtime client."""
        self.realtime_client: Optional[AsyncRealtimeClient] = None
        self.channels: dict[str, any] = {}  # channel_name -> channel object
        self.is_connected: bool = False
        self.reconnect_attempts: int = 0
        self.max_reconnect_attempts: int = 10
        self.reconnect_delay: float = 1.0  # Start with 1 second
        self.max_reconnect_delay: float = 60.0  # Max 60 seconds
        
        # Supabase configuration
        self.supabase_url: Optional[str] = None
        self.supabase_key: Optional[str] = None
        self._init_config()
    
    def _init_config(self):
        """Initialize Supabase configuration."""
        supabase_url = getattr(settings, 'SUPABASE_URL', None)
        supabase_key = getattr(settings, 'SUPABASE_ANON_KEY', None)
        
        if not supabase_url or not supabase_key:
            logger.error(
                "Supabase credentials not configured. "
                "Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables."
            )
            return
        
        # Get the actual key value (handle SecretStr)
        if hasattr(supabase_key, 'get_secret_value'):
            key_value = supabase_key.get_secret_value()
        else:
            key_value = str(supabase_key)
        
        self.supabase_url = supabase_url
        self.supabase_key = key_value
        logger.info("✅ RealtimeListener: Supabase configuration initialized")
    
    async def connect(self) -> bool:
        """Connect to Supabase Realtime."""
        if not REALTIME_AVAILABLE:
            logger.error("Cannot connect: realtime-py library not installed")
            return False
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("Cannot connect: Supabase configuration not initialized")
            return False
        
        try:
            # Extract host from Supabase URL
            # URL format: https://project-id.supabase.co
            host = self.supabase_url.replace('https://', '').replace('http://', '')
            realtime_url = f"wss://{host}/realtime/v1"
            
            # Create Realtime client
            # Note: token parameter is used for authentication
            self.realtime_client = AsyncRealtimeClient(
                realtime_url,
                token=self.supabase_key
            )
            
            # Connect
            await self.realtime_client.connect()
            self.is_connected = True
            logger.info("✅ RealtimeListener: Connected to Supabase Realtime")
            return True
        except Exception as e:
            logger.error(f"❌ RealtimeListener: Connection failed: {e}", exc_info=True)
            self.is_connected = False
            return False
    
    async def subscribe_to_section_states(
        self,
        user_id: int,
        thread_id: str,
        callback: Callable[[dict], None]
    ) -> Optional[str]:
        """
        Subscribe to section_states table changes for a specific thread.
        
        Args:
            user_id: User ID
            thread_id: Thread ID
            callback: Function to call when event is received
        
        Returns:
            Channel name if successful, None otherwise
        """
        if not self.realtime_client or not self.is_connected:
            logger.error("Cannot subscribe: Realtime client not connected")
            return None
        
        channel_name = f"section_states:{thread_id}"
        
        # Unsubscribe if already subscribed
        if channel_name in self.channels:
            await self.unsubscribe(channel_name)
        
        try:
            # Create channel
            channel = self.realtime_client.channel(channel_name)
            
            # Subscribe to postgres_changes events
            # Note: Using thread_id only since it's unique per conversation
            # PostgREST filter syntax uses & for multiple conditions, but Realtime may not support it
            # Signature: on_postgres_changes(event, callback, table=None, schema=None, filter=None)
            channel.on_postgres_changes(
                "*",  # event: INSERT, UPDATE, DELETE, or *
                lambda payload: self._handle_event(payload, callback),  # callback
                table="section_states",  # table name
                schema="public",  # schema name
                filter=f"thread_id=eq.{thread_id}"  # filter condition
            )
            
            # Subscribe to channel
            await channel.subscribe()
            self.channels[channel_name] = channel
            
            logger.info(
                f"✅ RealtimeListener: Subscribed to section_states for "
                f"user_id={user_id}, thread_id={thread_id}"
            )
            
            return channel_name
        except Exception as e:
            logger.error(f"❌ RealtimeListener: Subscription failed: {e}", exc_info=True)
            return None
    
    async def subscribe_to_business_plans(
        self,
        user_id: int,
        thread_id: str,
        callback: Callable[[dict], None]
    ) -> Optional[str]:
        """
        Subscribe to business_plans table changes for a specific thread.
        
        Args:
            user_id: User ID
            thread_id: Thread ID
            callback: Function to call when event is received
        
        Returns:
            Channel name if successful, None otherwise
        """
        if not self.realtime_client or not self.is_connected:
            logger.error("Cannot subscribe: Realtime client not connected")
            return None
        
        channel_name = f"business_plans:{thread_id}"
        
        # Unsubscribe if already subscribed
        if channel_name in self.channels:
            await self.unsubscribe(channel_name)
        
        try:
            # Create channel
            channel = self.realtime_client.channel(channel_name)
            
            # Subscribe to postgres_changes events
            # Note: Using thread_id only since it's unique per conversation
            # Signature: on_postgres_changes(event, callback, table=None, schema=None, filter=None)
            channel.on_postgres_changes(
                "*",  # event: INSERT, UPDATE, DELETE, or *
                lambda payload: self._handle_event(payload, callback),  # callback
                table="business_plans",  # table name
                schema="public",  # schema name
                filter=f"thread_id=eq.{thread_id}"  # filter condition
            )
            
            # Subscribe to channel
            await channel.subscribe()
            self.channels[channel_name] = channel
            
            logger.info(
                f"✅ RealtimeListener: Subscribed to business_plans for "
                f"user_id={user_id}, thread_id={thread_id}"
            )
            
            return channel_name
        except Exception as e:
            logger.error(f"❌ RealtimeListener: Subscription failed: {e}", exc_info=True)
            return None
    
    def _handle_event(self, payload: dict, callback: Callable[[dict], None]):
        """Handle Realtime event and call callback."""
        try:
            # Log full payload structure for debugging
            logger.info(f"🔔 RealtimeListener: Received event")
            logger.info(f"📦 Payload keys: {list(payload.keys())}")
            logger.debug(f"📦 Full payload: {payload}")
            
            # realtime-py sends payload in a nested structure
            # Extract the actual data from the payload
            actual_payload = payload
            
            # Check if payload has nested structure (realtime-py format)
            if "payload" in payload:
                actual_payload = payload["payload"]
            elif "data" in payload:
                actual_payload = payload["data"]
            
            # Log extracted payload
            logger.info(f"📦 Extracted payload keys: {list(actual_payload.keys()) if isinstance(actual_payload, dict) else 'Not a dict'}")
            
            callback(actual_payload)
            logger.info(f"✅ RealtimeListener: Event callback executed successfully")
        except Exception as e:
            logger.error(f"❌ RealtimeListener: Error handling event: {e}", exc_info=True)
    
    async def unsubscribe(self, channel_name: str) -> bool:
        """
        Unsubscribe from a channel.
        
        Args:
            channel_name: Name of the channel to unsubscribe from
        
        Returns:
            True if successful, False otherwise
        """
        if channel_name not in self.channels:
            logger.warning(f"Channel {channel_name} not found in subscriptions")
            return False
        
        try:
            channel = self.channels[channel_name]
            await channel.unsubscribe()
            del self.channels[channel_name]
            logger.info(f"✅ RealtimeListener: Unsubscribed from {channel_name}")
            return True
        except Exception as e:
            logger.error(f"❌ RealtimeListener: Unsubscribe failed: {e}", exc_info=True)
            return False
    
    async def disconnect(self):
        """Disconnect from all channels."""
        channel_names = list(self.channels.keys())
        for channel_name in channel_names:
            await self.unsubscribe(channel_name)
        
        if self.realtime_client:
            try:
                await self.realtime_client.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting Realtime client: {e}")
        
        self.is_connected = False
        logger.info("✅ RealtimeListener: Disconnected from all channels")
    
    async def reconnect(self) -> bool:
        """Reconnect with exponential backoff."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(
                f"Max reconnection attempts ({self.max_reconnect_attempts}) reached. "
                "Stopping reconnection attempts."
            )
            return False
        
        self.reconnect_attempts += 1
        delay = min(self.reconnect_delay * (2 ** (self.reconnect_attempts - 1)), self.max_reconnect_delay)
        
        logger.info(f"Reconnecting in {delay:.1f} seconds (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})...")
        await asyncio.sleep(delay)
        
        # Disconnect all channels
        await self.disconnect()
        
        # Reconnect
        success = await self.connect()
        
        if success:
            # Resubscribe to all channels
            # Note: We need to store callback info to resubscribe
            # This is a simplified version - in production, store subscription info
            logger.info("✅ RealtimeListener: Reconnected successfully")
            self.reconnect_attempts = 0
            self.reconnect_delay = 1.0
            return True
        else:
            return await self.reconnect()  # Retry
    
    def get_subscription_count(self) -> int:
        """Get number of active subscriptions."""
        return len(self.channels)

