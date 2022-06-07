#!/bin/python3

from DiscordBot import Bot
from Classes import Configuration

if __name__ == '__main__':
    conf = Configuration()
    client = Bot(conf=conf)
    client.run()
