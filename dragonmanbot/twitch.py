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
        self.listeners = []

    def chat(self, message):
        self.socket.send("PRIVMSG #{} :{}\r\n".format(self.channel, message).encode("utf-8"))

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.send("PASS {}\r\n".format(self.oauth).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.nick).encode("utf-8"))
        self.socket.send("JOIN #{}\r\n".format(self.channel).encode("utf-8"))
        print("Connected")

    def parse(self, response):
        message_format = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = message_format.sub("", response)
        message = message.rstrip()

        return {"username": username, "message": message}

    def process_message(self, message):
        for function in self.listeners:
            response = function(message)
            if response != None:
                self.chat(response)

        command_format = r"^(!\w+)(.*)"
        user_command = re.search(command_format, message["message"])
        if user_command != None:
            for command, function in self.commands.items():
                if user_command.group(1) == command:
                    response = function(user_command.group(2), message)
                    if response != None:
                        self.chat(response)

    def register_command(self, command, function):
        self.commands[command] = function

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
                    print(f'{message["username"]}: {message["message"]}')
                    self.process_message(message)
            time.sleep(0.1)                    