import logging
import time

from .base import BaseLoop


logger = logging.getLogger(__name__)


class StatusLoop(BaseLoop):
    loop_time = 0.1  # 10hz

    def run_loop(self):
        logger.info('status looped at: %s', time.time())


loop = StatusLoop()
