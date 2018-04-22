import logging
import time

import curio

logger = logging.getLogger(__name__)


class BaseTask:
    loop_time = 1  # 1hz
    frequency = None

    def __init__(self):
        if hasattr(self, 'frequency'):
            self.loop_time = 1 / self.frequency

    @classmethod
    def run(cls):
        return cls().do_loop

    async def do_loop(self, feed):
        # self.data = data
        self.feed = feed
        try:
            await self.setup()
            end_time = None
            while True:
                start_time = time.time()
                await self.run_loop(last_run=end_time)
                end_time = time.time()

                elapsed_time = (end_time - start_time)
                diff = max(self.loop_time - elapsed_time, 0)
                if elapsed_time > self.loop_time:
                    logger.warning(
                        '%s Ran over by %s!',
                        self.__class__.__name__,
                        elapsed_time - self.loop_time
                    )
                await curio.sleep(diff)
        # TODO: handle setup and loop errors
        except curio.CancelledError:
            await self.cleanup()

    async def publish(self, *args, **kwargs):
        await self.feed.publish(*args, **kwargs)

    async def setup(self):
        """Setup is complete if we don't error"""
        logger.info('setup for %s', self.__class__.__name__)
        pass

    async def cleanup(self):
        """Cleaning up loop when we're canceling the event loop"""
        logger.info('cleanup for %s', self.__class__.__name__)
        pass

    async def run_loop(self, **kwargs):
        raise NotImplementedError('run_loop needs implemented')
