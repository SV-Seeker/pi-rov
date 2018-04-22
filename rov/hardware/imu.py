import random

from Adafruit_BNO055 import BNO055

# RST connected to pin P9_12:
RESET_PIN = 'P9_12'


class BaseIMU:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BNOIMU(BNO055.BNO055, BaseIMU):

    def load_calibration(self, filename):
        """Read the internal calibration paramters from a json file.
        :param filename: path to the calibration file
        """
        import json
        with open(filename) as f:
            json_data = json.load(f)

        data = []
        data_fields = ['acc_offset', 'mag_offset', 'gyro_offset', 'acc_radius',
                       'mag_radius']
        for f in data_fields:
            if isinstance(json_data[f], list):
                for v in json_data[f]:
                    data.append(v & 0xFF)
                    data.append(v >> 8 & 0xFF)
            else:
                data.append(json_data[f] & 0xFF)
                data.append(json_data[f] >> 8 & 0xFF)

        self.set_calibration(data)

    def write_calibration(self, filename):
        """Write the internal calibration parameters to a json file.
        :param filename: where to save the calibration file
        """
        import json
        from datetime import datetime
        data = self.get_calibration()
        data = [((data[i * 2 + 1] << 8) | data[i * 2]) & 0xFFFF for i in range(11)]
        json_data = {
            'date': datetime.now().isoformat(),
            'acc_offset': data[0:3],
            'mag_offset': data[3:6],
            'gyro_offset': data[6:9],
            'acc_radius': data[9],
            'mag_radius': data[10]
        }
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4, sort_keys=True)


class FakeIMU(BaseIMU):
    """Fake methods for testing"""

    calibrated = False

    def get_calibration_status(self):
        sys = 3 if self.calibrated else 0
        gyro = 3 if self.calibrated else 0
        accel = 3 if self.calibrated else 0
        mag = 3 if self.calibrated else 0
        return (sys, gyro, accel, mag)

    def read_euler(self):
        return (random.randint(0, 500), random.randint(0, 500), random.randint(0, 500))


types = {
    'bno': BNOIMU,
    'fake': FakeIMU,
}


__all__ = ['types', 'BNOIMU', 'FakeIMU']
