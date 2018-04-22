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
    msg_id = 0  # id must be less than 32767

    def __init__(self, packed_value=None, **kwargs):
        packed_value = copy(packed_value)
        kwargs = copy(kwargs)
        keys = copy(self.struct_keys)
        # add msg_id key to the front
        keys = (('h', 'msg_id'),) + keys
        self.format, self.make_kwargs = zip(*keys)
        self.struct = struct.Struct(''.join(self.format))
        if packed_value:
            # parse message from passed value
            self.parse(packed_value)
        else:
            # build message from kwargs
            self.make(**kwargs)

    def upgrade(self):
        """upgrade message to correct msg class"""
        msg_id = self['msg_id']
        # no need to upgrade
        if self.msg_id != msg_id:
            return self
        # TODO: separate original bytes and packed_value
        return msg_map[msg_id](packed_value=self.packed_value)

    def order_values(self, **kwargs):
        key_map = dict(zip(self.make_kwargs, range(len(self.make_kwargs))))
        return [kwargs[i] for i in sorted(kwargs, key=key_map.__getitem__)]

    def make(self, **kwargs):
        self.value = kwargs
        kwargs.update({'msg_id': self.msg_id})
        self.packed_value = self.struct.pack(*self.order_values(**kwargs))
        return self.packed_value

    def parse(self, packed_value):
        self.packed_value = packed_value
        size = self.struct.size
        # crop off unneeded bits to prevent errors
        unpacked_value = self.struct.unpack(packed_value[:size])
        # left_over = packed_value[size:]
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


msg_map = {}
for msg_id, msg_type in enumerate(message_types, start=1):
    msg_type.msg_id = msg_id
    # register mapping between msg_id and type
    msg_map[msg_id] = msg_type
