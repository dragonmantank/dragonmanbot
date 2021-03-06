from dragonmanbot import session, twitchuser, twitch_http_client
import collections
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import random
import re

NEXT_NOTICE = datetime.now()
NEXT_NOTICE_COUNTER = 20

def reward_chat(message):
    if message["message"][:1] != "!":
        user = twitchuser.repository.findByUsername(message["username"])

        user.gold = user.gold + 1
        session.add(user)
        session.commit()

def display_notice(message):
    global NEXT_NOTICE_COUNTER
    global NEXT_NOTICE
    
    NEXT_NOTICE_COUNTER = NEXT_NOTICE_COUNTER - 1
    now = datetime.now()
    
    if now >= NEXT_NOTICE and NEXT_NOTICE_COUNTER < 1:
        fp = open("notices.txt")
        line = next(fp)
        NEXT_NOTICE = datetime.now() + timedelta(minutes=15)
        NEXT_NOTICE_COUNTER = 20
        
        for num, aline in enumerate(fp, 2):
            if random.randrange(num): continue
            line = aline
            fp.close()
            return line

        fp.close()

def log_chat(message):
    log = open("chatlog.txt", "a")
    log.write(message["raw"])
    log.close()

def announce_sub(message):
    parsed = re.search(r"display-name=(\w+);.*;msg-id=sub;.*msg-param-months=(\d+)", message["raw"])
    if parsed:
        username = parsed.group(1)
        months = int(parsed.group(2).rstrip())

        user = twitchuser.repository.findByUsername(username)
        user.gold = user.gold + 10000
        session.add(user)
        session.commit()

        log = open("latest_sub.txt", "w")
        log.write(user.username + "\r")
        log.close()

        if months > 1:
                return f"{username} has rejoined the clan for another month!"

        return f"{username} has joined the clan!"

def record_bits(message):
    parsed = re.search(r"bits=(\d+);.*display-name=(\w+);", message["raw"])
    if parsed:
        username = parsed.group(2)
        bits = int(parsed.group(1))

        user = twitchuser.repository.findByUsername(username)
        user.gold = user.gold + (bits * 10)
        session.add(user)
        session.commit()

        log = open("latest_bits.txt", "w")
        log.write(user.username + "\r")
        log.close()

def announce_raid(message):
    parsed = re.search(r"display-name=(\w+);.*;msg-id=raid;.*msg-param-viewerCount=(\d+);.*;user-id=(\d+)", message["raw"], re.DOTALL)
    if parsed:
        username = parsed.group(1)
        viewers = int(parsed.group(2))
        user_id = int(parsed.group(3))

        user = twitchuser.repository.findByUsername(username)
        user.gold = user.gold + (100 * viewers)
        session.add(user)
        session.commit()

        stream = twitch_http_client.channels.get_by_id(user_id)
        game = stream.game

        return f"{username} was playing \"{game}\" and is raiding with {viewers} viewers! Show some love and check them out some time! https://twitch.tv/{username}"