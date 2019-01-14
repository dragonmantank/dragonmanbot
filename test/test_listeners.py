import unittest
from unittest import mock
from unittest.mock import mock_open, patch
import socket
from dragonmanbot import twitch
from dragonmanbot import listener
from dragonmanbot import twitchuser
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

    # def test_notices_dont_display_with_time_left(self):
    #     listener.NEXT_NOTICE = datetime.now() - timedelta(minutes=5)
    #     listener.NEXT_NOTICE_COUNTER = -20

    #     response = listener.display_notice("message")
    #     self.assertFalse(response)

    def test_announce_sub(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            m = mock_open()
            with patch("builtins.open", unittest.mock.mock_open()) as m:
                mocked_return.return_value = twitchuser.TwitchUser(username="testuser", gold=100)
                message = "@badges=subscriber/0,premium/1;color=;display-name=testuser;emotes=;flags=;id=c9e5c49b-b53c-4ef3-859d-xxxxxxxxxxxx;login=testuser;mod=0;msg-id=sub;msg-param-months=1;msg-param-sub-plan-name=Channel\sSubscription\s(dragonmantank);msg-param-sub-plan=Prime;room-id=99999999;subscriber=1;system-msg=testuser\sjust\ssubscribed\swith\sTwitch\sPrime!;tmi-sent-ts=1546237570255;turbo=0;user-id=999999999;user-type= :tmi.twitch.tv USERNOTICE #dragonmantank"
                response = listener.announce_sub({"username": "", "message": "", "raw": message})
                
                self.assertEqual("testuser has joined the clan!", response)
                m.assert_called_once_with("latest_sub.txt", "w")
                handle = m()
                handle.write.assert_called_once_with('testuser\r')

    def test_announce_resubsub(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            m = mock_open()
            with patch("builtins.open", unittest.mock.mock_open()) as m:
                mocked_return.return_value = twitchuser.TwitchUser(username="testuser", gold=100)
                message = "@badges=subscriber/0,premium/1;color=;display-name=testuser;emotes=;flags=;id=c9e5c49b-b53c-4ef3-859d-xxxxxxxxxxxx;login=testuser;mod=0;msg-id=sub;msg-param-months=3;msg-param-sub-plan-name=Channel\sSubscription\s(dragonmantank);msg-param-sub-plan=Prime;room-id=99999999;subscriber=1;system-msg=testuser\sjust\ssubscribed\swith\sTwitch\sPrime!;tmi-sent-ts=1546237570255;turbo=0;user-id=999999999;user-type= :tmi.twitch.tv USERNOTICE #dragonmantank"
                response = listener.announce_sub({"username": "", "message": "", "raw": message})

                self.assertEqual("testuser has rejoined the clan for another month!", response)
                m.assert_called_once_with("latest_sub.txt", "w")
                handle = m()
                handle.write.assert_called_once_with('testuser\r')

    def test_record_bits(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            m = mock_open()
            with patch("builtins.open", unittest.mock.mock_open()) as m:
                mocked_return.return_value = twitchuser.TwitchUser(username="testuser", gold=100)
                message = "@badges=bits/100;bits=100;color=#8A2BE2;display-name=testuser;emotes=;flags=;id=712ab0ee-b727-4aa5-9b89-999999999999;mod=0;room-id=68573026;subscriber=0;tmi-sent-ts=1546840747770;turbo=0;user-id=99999999;user-type= :testuser!testuser@testuser.tmi.twitch.tv PRIVMSG #dragonmantank :cheer100"
                listener.record_bits({"username": "", "message": "", "raw": message})

                m.assert_called_once_with("latest_bits.txt", "w")
                handle = m()
                handle.write.assert_called_once_with('testuser\r')

    def test_announce_raid(self):
        with mock.patch("dragonmanbot.twitchuser.TwitchUserRepository.findByUsername") as mocked_return:
            mocked_return.return_value = twitchuser.TwitchUser(username="testuser", gold=100)
            message = "@badges=premium/1;color=#00FF7F;display-name=testuser;emotes=;flags=;id=7532d5b2-ddeb-4e85-992a-999999999999;login=testuser;mod=0;msg-id=raid;msg-param-displayName=testuser;msg-param-login=testuser;msg-param-profileImageURL=https://static-cdn.jtvnw.net/jtv_user_pictures/85896964-219d-4a32-837e-999999999999-profile_image-70x70.jpg;msg-param-viewerCount=7;room-id=68573026;subscriber=0;system-msg=7\sraiders\sfrom\testuser\shave\sjoined\n!;tmi-sent-ts=1547441871162;turbo=0;user-id=999999;user-type= :tmi.twitch.tv USERNOTICE #dragonmantank"
            response = listener.announce_raid({"username": "", "message": "", "raw": message})

            self.assertEqual("testuser is raiding with 7 viewers! Show some love and check them out some time!", response)