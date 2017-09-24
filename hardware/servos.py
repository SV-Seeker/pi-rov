# from math import radians
import logging

logger = logging.getLogger(__name__)


class BaseServo(object):
    """BaseServo functions"""
    def __init__(self, pwm, channel=0):
        try:
            self.debug = pwm.debug
        except:
            self.debug = False

        self.pwm = pwm
        self.channel = channel

        # check pwm
        self.min = 1000
        self.max = 2000
        self.range = ((self.max - self.min) / 2)
        self.mid = self.max - self.range
        self.cycle = 50 # 50hz cycle
        self.pulseLength = 1000000 / self.cycle
        self.tick = self.pulseLength / 4096 # 12 bit resolution

    def set_pulse(self, pulse):
        """set the pulse on this servo's channel"""
        pulse = max(min(pulse, self.max), self.min)
        self.pwm.setPWM(self.channel, 0, pulse/self.tick)


# class ContinuousServo(BaseServo):
#     """Continuous Servo"""
#     scale = 5
#     power = 0
#     flipped = 1
#     def __init__(self, *args, **kwargs):
#         if kwargs.pop('flipped', False):
#             self.flipped = -1
#         super(ContinuousServo, self).__init__(*args, **kwargs)
#
#     def set(self, point):
#         # never above 1 or below -1
#         point = max(min(point, 1.0), -1.0) * self.flipped
#         self.power = point
#         adjust = 0
#         if point != 0:
#             adjust = (point * self.range) / self.scale # scale down for more accurate control
#         newPulse = int(self.mid+adjust)
#         logger.debug('set_pulse %s, adjust: %s' % (newPulse, adjust))
#         self.set_pulse(newPulse)


class Servo(BaseServo):
    """Servo Handler"""
    def __init__(self, *args, total_deg=180, **kwargs):
        super(Servo, self).__init__(*args, **kwargs)
        self.total_deg = total_deg

    # functions to set angle and stuff
    # def radians(self, deg, minutes=0, sec=0):
    #     return radians(deg + minutes / 60.0 + sec / 3600.0)

    def _get_pulse_for_deg(self, deg):
        return (((self.max - self.min) * deg) / self.total_deg) + self.min

    def to_deg(self, deg):
        logger.debug("moving to %s degrees" % deg)
        self.set_pulse(self._get_pulse_for_deg(deg))
