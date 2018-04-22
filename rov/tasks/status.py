import logging
import time

from .base import BaseTask

logger = logging.getLogger(__name__)


class StatusTask(BaseTask):
    """
    Craft status changes
    data from imu and different toggles
    heading, speed, status, warnings
    """
    frequency = 10  # hz

    async def run_loop(self, **kwargs):
        logger.debug('status looped at: %s', time.time())
        # Push statuses to any listening clients
        # await self.publish(b'status update\n')
