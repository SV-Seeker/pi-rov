class BaseLoop:
    loop_time = 1  # 1hz

    def setup(self):
        """setup is complete if we don't error"""

    def run_loop(self):
        raise NotImplementedError('run_loop needs implemented')

    def get_add_parameters(self):
        """loop add parameters"""
        return (self.run_loop, self.loop_time)
