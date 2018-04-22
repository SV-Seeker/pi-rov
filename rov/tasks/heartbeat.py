import logging
import time

from .base import BaseTask

logger = logging.getLogger(__name__)


class HeartbeatTask(BaseTask):
    frequency = 1  # 1hz

    async def run_loop(self, **kwargs):
        logger.debug('heartbeat task ran at: %s', time.time())

        # TODO: heartbeat hash should send up some beat id or hash so the upside
        # can respond with a reciprocal message, to determine the beat was received.
        await self.publish(b'beat\n')
