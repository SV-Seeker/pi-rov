import curio
import logging


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
            while True:
                await self.run_loop()
                await curio.sleep(self.loop_time)
        # TODO: handle setup and loop errors
        except curio.CancelledError:
            await self.cleanup()

    async def publish(self, *args, **kwargs):
        await self.feed.publish(*args, **kwargs)

    async def setup(self):
        """Setup is complete if we don't error"""
        pass

    async def cleanup(self):
        """Cleaning up loop when we're canceling the event loop"""
        logger.info('cleanup for %s', self.__class__.__name__)
        pass

    async def run_loop(self):
        raise NotImplementedError('run_loop needs implemented')
