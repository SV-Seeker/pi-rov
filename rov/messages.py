import struct
from collections.abc import Mapping
from copy import copy

EXIT = b'x'


class Message(Mapping):
    """
    automatically create a formatted byte message that can be shared
    and formatted/parsed,
    convert a message into bytes, and also parse it

    TODO:
    * allow for default values, (msg version, dynamic fields for mixins)
    * error handling/exceptions for missing arguments
    * attribute for a message key that is unique across all messages.
    """
    struct_keys = tuple()

    def __init__(self, packed_value=None, **kwargs):
        self.format, self.make_kwargs = zip(*self.struct_keys)
        self.struct = struct.Struct(''.join(self.format))
        if packed_value:
            # parse message from passed value
            self.parse(packed_value)
        else:
            # build message from kwargs
            self.make(**kwargs)

    def order_values(self, **kwargs):
        key_map = dict(zip(self.make_kwargs, range(len(self.make_kwargs))))
        return [kwargs[i] for i in sorted(kwargs, key=key_map.__getitem__)]

    def make(self, **kwargs):
        self.value = kwargs
        self.packed_value = self.struct.pack(*self.order_values(**kwargs))
        return self.packed_value

    def parse(self, packed_value):
        self.packed_value = packed_value
        unpacked_value = self.struct.unpack(packed_value)
        self.value = self.assemble_value(unpacked_value)
        return self.value

    def assemble_value(self, unpacked_value):
        return dict(zip(self.make_kwargs, unpacked_value))

    def __str__(self):
        # TODO: str rep
        pass

    def __bytes__(self):
        return self.packed_value

    def __contains__(self, value):
        return value in self.value.keys()

    def __iter__(self):
        return iter(self.value)

    def __getitem__(self, value):
        return self.value[value]

    def __len__(self):
        return len(self.value)


class SetupMessage(Message):
    struct_keys = (
        ('f', 'heading'),
        ('f', 'roll'),
        ('f', 'pitch'),
        ('i', 'sys'),
        ('i', 'gyro'),
        ('i', 'accel'),
        ('i', 'mag'),
        ('?', 'callibration'),
    )


class IMUMessage(Message):
    struct_keys = (
        ('i', 'heading'),
        ('i', 'roll'),
        ('i', 'pitch'),
    )


message_types = Message.__subclasses__()