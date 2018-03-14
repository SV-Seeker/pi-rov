import curio


class BaseTask:
    loop_time = 1  # 1hz

    @classmethod
    def run(cls):
        return cls().do_loop

    async def do_loop(self, publish):
        # self.data = data
        self.publish = publish
        try:
            self.setup()
            while True:
                await self.run_loop()
                await curio.sleep(self.loop_time)
        except curio.CancelledError:
            self.cleanup()

    def setup(self):
        """Setup is complete if we don't error"""
        pass

    def cleanup(self):
        """Cleaning up loop when we're canceling the event loop"""
        pass

    async def run_loop(self):
        raise NotImplementedError('run_loop needs implemented')
