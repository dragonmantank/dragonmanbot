import unittest
from unittest import mock
import dragonmanbot
from dragonmanbot import twitchuser

class TestTwitchUser(unittest.TestCase):
    def test_get_user(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="bob", gold=100)
            user = twitchuser.repository.findByUsername(username="bob")
            self.assertEqual("bob", user.username)
            self.assertEqual(100, user.gold)
