import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twitch import TwitchClient

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config["database"]["dsn"])
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
twitch_http_client = TwitchClient(client_id=config["twitch"]["clientid"])

from dragonmanbot import command