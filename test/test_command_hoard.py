import unittest
from unittest import mock
import dragonmanbot
from dragonmanbot import twitchuser
from dragonmanbot import command

class TestCommandHoard(unittest.TestCase):
    def test_get_user(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="bob", gold=100)
            message = {"username": "bob", "message": "!hoard"}
            response = command.command_hoard("!hoard", message)
            self.assertEqual("@bob You have amassed 100 gold!", response)
