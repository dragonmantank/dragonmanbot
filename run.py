from dragonmanbot import bot
from dragonmanbot import session
from dragonmanbot import twitchuser
from dragonmanbot import command
from dragonmanbot import listener
import configparser
import argparse

if __name__ == "__main__":
    config = configparser.ConfigParser();
    config.read('config.ini')

    bot = bot.Dragonmanbot(config['twitch']['nick'], config['twitch']['channel'], config['twitch']['oauth'])
    bot.register_listener(listener.reward_chat)
    bot.register_command("!hoard", command.command_hoard)
    bot.run()