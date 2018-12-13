import unittest
from unittest import mock
import socket
from dragonmanbot import twitch
from dragonmanbot import listener
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

class TestListeners(unittest.TestCase):
    def test_notices_display_at_appropriate_time(self):
        listener.NEXT_NOTICE = datetime.now() - timedelta(minutes=50)
        listener.NEXT_NOTICE_COUNTER = 0

        response = listener.display_notice("message")
        self.assertTrue(response)

    def test_notices_dont_display_with_counter_left(self):
        listener.NEXT_NOTICE = datetime.now() - timedelta(minutes=50)
        listener.NEXT_NOTICE_COUNTER = 10

        response = listener.display_notice("message")
        self.assertFalse(response)

    def test_notices_dont_display_with_time_left(self):
        listener.NEXT_NOTICE = datetime.now() - timedelta(minutes=10)
        listener.NEXT_NOTICE_COUNTER = -20

        response = listener.display_notice("message")
        self.assertFalse(response)