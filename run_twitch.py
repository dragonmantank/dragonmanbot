from dragonmanbot import twitch
from dragonmanbot import session
from dragonmanbot import twitchuser
from dragonmanbot import command
from dragonmanbot import listener
from dragonmanbot import discord
import configparser
import argparse

if __name__ == "__main__":
    config = configparser.ConfigParser();
    config.read('config.ini')

    twitchBot = twitch.Dragonmanbot(config['twitch']['nick'], config['twitch']['channel'], config['twitch']['oauth'])
    twitchBot.register_listener(listener.reward_chat)
    twitchBot.register_listener(listener.log_chat)
    twitchBot.register_listener(listener.display_notice)
    twitchBot.register_command("!hoard", command.command_hoard)
    twitchBot.register_command_alias("!points", "!hoard")
    twitchBot.register_command_alias("!coins", "!hoard")
    twitchBot.register_command_alias("!gold", "!hoard")
    twitchBot.register_command("!discord", command.command_discord)
    twitchBot.register_command("!name", command.command_namerequest)
    twitchBot.register_command("!gamerequest", command.command_gamerequest)
    twitchBot.register_command("!coin", command.command_coinflip)
    twitchBot.run()
