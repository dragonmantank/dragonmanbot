from dragonmanbot import session, twitchuser

def reward_chat(message):
    if message["message"][:1] != "!":
        user = twitchuser.repository.findByUsername(message["username"])

        user.gold = user.gold + 1
        session.add(user)
        session.commit()