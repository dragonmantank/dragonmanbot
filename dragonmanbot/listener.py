from dragonmanbot import session, twitchuser
import collections
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import random

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
