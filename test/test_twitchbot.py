import unittest
from unittest import mock
import socket
from dragonmanbot import twitch

class TestTwitchBot(unittest.TestCase):
    def test_cmd_list(self):
        with mock.patch("socket.socket") as mocked_socket:
            mocked_socket.return_value.recv.side_effect = [
                b"@badges=broadcaster/1,subscriber/0;color=;display-name=dragonmantank;emotes=;flags=;id=e38cbcfc-42e9-4f41-927b-aaaaaaaaaaaa;mod=0;room-id=99999999;subscriber=1;tmi-sent-ts=1547354057275;turbo=0;user-id=99999999;user-type= :dragonmantank!dragonmantank@dragonmantank.tmi.twitch.tv PRIVMSG #dragonmantank :!cmd", 
                socket.error
            ]
            try:
                def fakecommand():
                    pass

                twitchBot = twitch.Dragonmanbot("nick", "channel", "oauth")
                twitchBot.register_command("!fake", fakecommand)
                twitchBot.run()
            except:
                pass

            twitchBot.socket.connect.assert_called_with(("irc.twitch.tv", 6667))
            expected = "PRIVMSG #{} :{}\r\n".format("channel", "@dragonmantank here are the available commands: !cmd, !fake")
            twitchBot.socket.send.assert_called_with(bytearray(expected, "utf-8"))
            
