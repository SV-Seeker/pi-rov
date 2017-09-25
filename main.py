# Main loop of the ROV
from time import sleep
import logging
from scheduler import LoopScheduler

from loops import (
    control_loop,
    heartbeat_loop,
    status_loop,
)

# DEBUG
# import sys
# import fake_rpi
# sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
# sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Scheduling events
# set time delay callbacks for the different proceedures
looper = LoopScheduler()

# Add loop handlers and run their setups
looper.add_loop(control_loop)
looper.add_loop(heartbeat_loop)
looper.add_loop(status_loop)
looper.setup()


logger.info('starting loop')
while True:
    try:
        looper.run(blocking=False)
        sleep(looper.time_till_next)
    except KeyboardInterrupt:
        logger.info('User shutdown of ROV loop')
        raise
    except Exception as error:
        logger.info('Error occured: %s', error)
        raise
    # finally:
    #     logger.info('shutting down ROV loop')
