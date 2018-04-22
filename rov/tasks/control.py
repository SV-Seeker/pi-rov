import logging
import time

# import curio
from catalog import Catalog, CatalogMember
from config import config
from hardware.imu import types as imu_types
from redis import client

from .base import BaseTask

logger = logging.getLogger(__name__)


class Control:

    class Modes(Catalog):
        _attrs = 'value', 'label'
        absolute = 0, 'Absolute'
        locked = 1, 'Locked'

    mode = Modes.absolute

    def switch_mode(self, mode, lookup='value'):
        if isinstance(CatalogMember, mode):
            self.mode = mode
        else:
            self.mode = self.Modes(mode, lookup)


class ControlTask(BaseTask):
    frequency = 20  # hz

    def __init__(self):
        imu_type = config.get('imu')
        IMU = imu_types.get(imu_type)

        self.imu = IMU()

    async def callibrate_imu(self):
        # calibration_data = self.imu.get_calibration_status()
        # sys, gyro, accel, mag = calibration_data
        # heading, roll, pitch = self.imu.read_euler()
        # needs_callibration = min(*calibration_data) <= 2

        # # setup_msg = imu_capnp.IMUSetup.new_message(
        # #     gyro=dict(
        # #         heading=heading, roll=roll, pitch=pitch
        # #     ),
        # #     callibration=dict(
        # #         sys=sys, gyro=gyro, accel=accel, mag=mag
        # #     ),
        # #     needsCallibration=needs_callibration
        # # )

        byte_msg = b''
        # byte_msg = setup_msg.to_bytes()
        await client.set(b'imu_setup', byte_msg)
        await self.publish(byte_msg)

    async def setup(self):
        await self.callibrate_imu()
        await super().setup()

    async def cleanup(self):
        # TODO: save imu callibration items or next start instructions to redis.
        await super().setup()

    async def run_loop(self, **kwargs):
        """Run control loop and make adjustments to drive state"""
        # heading, roll, pitch = self.imu.read_euler()

        # imu_readings = bytes(imu_msg)
        # await client.set(b'imu', imu_readings)
        # await self.publish(imu_readings)
        logger.debug('control looped at: %s', time.time())
