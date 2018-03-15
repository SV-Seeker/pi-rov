import logging
import time

from .base import BaseTask


logger = logging.getLogger(__name__)


class HeartbeatTask(BaseTask):
    loop_time = 1  # 1hz

    async def run_loop(self):
        logger.debug('heartbeat task ran at: %s', time.time())
        await self.publish(b'beat\n')
        # beat = self.data.get('beats', 0)
        # self.data.update({'beats': beat + 1})
