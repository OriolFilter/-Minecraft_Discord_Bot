from Speaker import Bot
from Classes import Configuration


if __name__ == '__main__':
    conf = Configuration()
    client = Bot(conf=conf)
    client.run()


# Lacks error handling ...
# docker container
# multi arch docker container