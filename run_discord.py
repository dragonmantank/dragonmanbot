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

    discord.TOKEN = config["discord"]["token"]
    discord.run()
