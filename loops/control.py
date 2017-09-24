import logging
import time

from .base import BaseLoop
from hardware.imu import BNOIMU, FakeIMU

logger = logging.getLogger(__name__)


class ControlLoop(BaseLoop):
    loop_time = 0.05  # 20hz

    def __init__(self):
        # self.imu = BNOIMU()
        self.imu = FakeIMU()

    def setup(self):
        calibration_data = self.imu.get_calibration_status()
        sys, gyro, accel, mag = calibration_data
        heading, roll, pitch = self.imu.read_euler()
        logger.info(
            'IMU Info:'
            'Heading={0:0.2F} '
            'Roll={1:0.2F} '
            'Pitch={2:0.2F}'
            '\tSys_cal={3} '
            'Gyro_cal={4} '
            'Accel_cal={5}'
            'Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))
        # not a very good calibration
        if min(*calibration_data) <= 2:
            logger.warning('Calibration is not optimal!')
            # TODO: load configuration and try again.

    def run_loop(self):
        """Run control loop and make adjustments to drive state"""
        heading, roll, pitch = self.imu.read_euler()
        # logger.info('control looped at: %s', time.time())
        logger.info(heading)


loop = ControlLoop()
