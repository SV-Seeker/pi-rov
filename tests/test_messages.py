import unittest

import pytest
from mock import patch

from rov import messages


class TestMessage(unittest.TestCase):
    class NewMessage(messages.Message):
        struct_keys = (
            ('f', 'floaty'),
            ('?', 'booly'),
        )

    def test_init(self):
        pass

    def test_upgrade(self):
        pass

    def order_values(self):
        # values are ordered by the struct key order
        # prevent normal init
        with patch('rov.messages.Message.__init__') as mock_init:
            msg = self.NewMessage(booly=False, floaty=1.4)
            result = msg.order_values()
            self.assertEqual(result, (1.4, False))
