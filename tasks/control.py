import logging
import time

from .base import BaseTask
from messages import SetupMessage, IMUMessage
from hardware.imu import BNOIMU, FakeIMU


logger = logging.getLogger(__name__)


class ControlTask(BaseTask):
    frequency = 20  # hz

    def __init__(self):
        # self.imu = BNOIMU()
        self.imu = FakeIMU()

    async def setup(self):
        calibration_data = self.imu.get_calibration_status()
        sys, gyro, accel, mag = calibration_data
        heading, roll, pitch = self.imu.read_euler()
        callibration = min(*calibration_data) <= 2
        msg = SetupMessage(
            sys=sys, gyro=gyro, accel=accel, mag=mag, heading=heading,
            roll=roll, pitch=pitch, callibration=callibration)
        await self.publish(bytes(msg))

    async def run_loop(self):
        """Run control loop and make adjustments to drive state"""
        heading, roll, pitch = self.imu.read_euler()
        msg = IMUMessage(heading=heading, roll=roll, pitch=pitch)
        await self.publish(bytes(msg))
        logger.debug('control looped at: %s', time.time())
        logger.debug("%s,%s,%s", heading, roll, pitch)
