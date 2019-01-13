import dragonmanbot
import random

def command_namerequest(command, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])
    if user.gold >= 500:
        user.gold = user.gold - 500
        dragonmanbot.twitchuser.repository.save(user)
        log = open("names.txt", "a")
        log.write(user.username + "\r")
        log.close()

        return f"@{message['username']} You've just made the list! List3"
    
    return f"@{message['username']} You need at least 500 gold to request a name in the game (check with !hoard)"

def command_gamerequest(game, message):
    game = ' '.join(game)
    game_file = open('games.txt', 'a')
    game_file.write(game + "\n")
    game_file.close()
    return f"@{message['username']} Game has been added to the list"

def command_coinflip(arguments, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])
    if len(arguments) == 0:
        return f"@{message['username']} You have to specify an amount of coins to bet!"

    amount = arguments[0]
    if arguments[0] == "all":
        amount = user.gold
    amount = int(amount)

    if amount <= user.gold:
        if random.randint(0,10) % 2 == 0:
            user.gold = user.gold + amount
            dragonmanbot.twitchuser.repository.save(user)
            return f"@{message['username']} flips the coin and wins {amount}!"
        else:
            user.gold = user.gold - amount
            dragonmanbot.twitchuser.repository.save(user)
            return f"@{message['username']} flips the coin and loses {amount}!"
    else:
        return f"@{message['username']} You can't bet that much!"

def command_hoard(command, message):
    user = dragonmanbot.twitchuser.repository.findByUsername(message["username"])
    return f'@{message["username"]} You have amassed {user.gold} gold!'

def command_discord(command, message):
    return f'Want to hang out on discord? Head over to https://discord.gg/PZ9fX2g !'