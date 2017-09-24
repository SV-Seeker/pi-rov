import logging
import time

from .base import BaseLoop


logger = logging.getLogger(__name__)


class HeartbeatLoop(BaseLoop):
    loop_time = 1  # 1hz

    def run_loop(self):
        logger.info('heartbeat looped at: %s', time.time())


loop = HeartbeatLoop()
