#!/bin/python3

from Speaker import Bot
from Classes import Configuration


if __name__ == '__main__':
    conf = Configuration()
    client = Bot(conf=conf)
    client.run()