import socket
import time
import errno
import sys
import re

class Dragonmanbot:
    def __init__(self, nick, channel, oauth, host="irc.twitch.tv", port="6667"):
        self.host = host
        self.port = int(port)
        self.nick = nick
        self.channel = channel
        self.oauth = oauth
        self.commands = {}
        self.command_aliases = {}
        self.listeners = []

        self.register_command("!cmd", self.command_listcommands)

    def chat(self, message):
        self.socket.send("PRIVMSG #{} :{}\r\n".format(self.channel, message).encode("utf-8"))

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.send("CAP REQ :twitch.tv/commands twitch.tv/membership twitch.tv/tags\r\n".encode("utf-8"))
        self.socket.send("PASS {}\r\n".format(self.oauth).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.nick).encode("utf-8"))
        self.socket.send("JOIN #{}\r\n".format(self.channel).encode("utf-8"))
        print("Connected")

    def parse(self, response):
        username = message = ''
        parsed = re.search(r"display-name=(\w+);.*PRIVMSG #\w+ :(.*)$", response)
        if parsed:
            username = parsed.group(1)
            message = parsed.group(2).rstrip()

        return {"username": username, "message": message, "raw": response}

    def process_message(self, message):
        for function in self.listeners:
            response = function(message)
            if response != None:
                self.chat(response)

        command_format = r"^(!\w+)(.*)"
        user_command = re.search(command_format, message["message"])
        if user_command != None:
            command = user_command.group(1)
            if command in self.command_aliases:
                command = self.command_aliases[command]

            if command in self.commands:
                response = self.commands[command](user_command.group(2).split(), message)
                if response != None:
                    self.chat(response)

    def command_listcommands(self, command, message):
        commands = list(self.commands.keys())
        command_list = ", ".join(commands)
        return f'@{message["username"]} here are the available commands: {command_list}'

    def register_command(self, command, function):
        self.commands[command] = function

    def register_command_alias(self, alias, command):
        self.command_aliases[alias] = command

    def register_listener(self, function):
        self.listeners.append(function)

    def run(self):
        self.connect()
        while True:
            try:
                response = self.socket.recv(1024).decode("utf-8")
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:
                if response == "PING :tmi.twitch.tv\r\n":
                    self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                else:
                    message = self.parse(response)
                    if message['username'] and message['message']:
                        print(f'{message["username"]}: {message["message"]}')
                    else:
                        print(f'{message["raw"]}')

                    self.process_message(message)
            time.sleep(0.1)                    