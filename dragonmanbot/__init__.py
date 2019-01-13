import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config["database"]["dsn"])
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

from dragonmanbot import command