import dragonmanbot

NAMES = []

def command_namerequest(command, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])
    if user.gold >= 500:
        user.gold = user.gold - 500
        dragonmanbot.twitchuser.repository.save(user)
        return f"@{message['username']} You've just made the list! List3"
    
    return f"@{message['username']} You need at least 500 gold to request a name in the game"
    

def command_hoard(command, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])
    return f'@{message["username"]} You have amassed {user.gold} gold!'

def command_discord(command, message):
    return f'Want to hang out on discord? Head over to https://discord.gg/PZ9fX2g !'