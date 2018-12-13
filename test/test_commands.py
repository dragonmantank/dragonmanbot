import unittest
from unittest import mock
import dragonmanbot
from dragonmanbot import twitchuser
from dragonmanbot import command

class TestCommands(unittest.TestCase):
    def test_get_hoard(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="bob", gold=100)
            message = {"username": "bob", "message": "!hoard"}
            response = command.command_hoard("!hoard", message)
            self.assertEqual("@bob You have amassed 100 gold!", response)

    def test_empty_coinflip(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="bob", gold=100)
            message = {"username": "bob", "message": "!coin"}
            response = command.command_coinflip([], message)
            self.assertEqual("@bob You have to specify an amount of coins to bet!", response)

    def test_coinflip(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="bob", gold=100)
            message = {"username": "bob", "message": "!coin 10"}
            response = command.command_coinflip(["10"], message)

