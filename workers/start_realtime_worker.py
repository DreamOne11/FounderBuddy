#!/usr/bin/env python3
"""Start Realtime Worker - Entry point for Realtime worker process."""

import asyncio
import signal
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from core.logging_config import setup_logging, get_logger
from core.settings import settings
from integrations.supabase.realtime_worker import RealtimeWorker

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Global worker instance
worker: RealtimeWorker | None = None


def signal_handler(sig, frame):
    """Handle shutdown signals."""
    logger.info("Received shutdown signal, stopping worker...")
    if worker:
        asyncio.create_task(worker.stop())
    sys.exit(0)


async def main():
    """Main entry point."""
    global worker
    
    # Check if Realtime is enabled
    if not settings.USE_SUPABASE_REALTIME:
        logger.warning(
            "USE_SUPABASE_REALTIME is False. "
            "Set USE_SUPABASE_REALTIME=true to enable Realtime worker."
        )
        return
    
    # Check Supabase configuration
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        logger.error(
            "Supabase configuration missing. "
            "Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables."
        )
        return
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start worker
    worker = RealtimeWorker()
    
    try:
        await worker.start()
        
        if not worker.is_running:
            logger.error("Failed to start worker")
            return
        
        logger.info("✅ Realtime Worker started successfully")
        logger.info(f"Worker status: running={worker.is_running}")
        
        # Keep running until stopped
        while worker.is_running:
            await asyncio.sleep(1)
            
            # Health check
            if not await worker.health_check():
                logger.warning("Worker health check failed, attempting reconnection...")
                await worker.stop()
                await asyncio.sleep(5)
                await worker.start()
    
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, stopping worker...")
    except Exception as e:
        logger.error(f"❌ Worker error: {e}", exc_info=True)
    finally:
        if worker:
            await worker.stop()
        logger.info("Realtime Worker stopped")


if __name__ == "__main__":
    asyncio.run(main())




