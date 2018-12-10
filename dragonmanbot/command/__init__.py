import dragonmanbot

def command_hoard(command, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])

    return f'@{message["username"]} You have amassed {user.gold} gold!'