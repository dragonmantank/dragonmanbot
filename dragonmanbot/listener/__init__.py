from dragonmanbot import session, twitchuser
import collections

def reward_chat(message):
    if message["message"][:1] != "!":
        user = twitchuser.repository.findByUsername(message["username"])

        user.gold = user.gold + 1
        session.add(user)
        session.commit()

def log_chat(message):
    log = open("chatlog.txt", "a")
    log.write(message["raw"])
    log.close()
