

import struct
import binascii

class Message:
    """
    automatically create a formatted byte message that can be shared
    and formatted/parsed,
    convert a message into bytes, and also parse it
    """

    def __init__(self):
        structs, kwargs = zip(**self.struct_keys)
        self.packer = struct.Struct(' '.join(structs))

    def parse(msg):
        pass

    def __str__(self):
        return binascii.hexlify(packed_data)

    def __bytes__(self):
        return self.packer.pack(*values)


class SetupMessage(Message):
    struct_keys = (
        ('f', 'heading'),
        ('f', 'roll'),
        ('f', 'pitch'),
        ('i', 'sys'),
        ('i', 'gyro'),
        ('i', 'accel'),
        ('i', 'mag'),
    )
