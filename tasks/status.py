import logging
import time

from .base import BaseTask


logger = logging.getLogger(__name__)


class StatusTask(BaseTask):
    loop_time = 0.1  # 10hz

    async def run_loop(self):
        logger.info('status looped at: %s', time.time())
        await self.publish(b'status update\n')
        # logger.info('had %s beats', self.data.get('beats', 0))
