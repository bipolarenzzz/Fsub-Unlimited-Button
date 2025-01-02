from bot import Bot
from asyncio import run
from pyrogram import Client

class Bot(Client):
    def __init__(self):
        super().__init__("my_bot")

if __name__ == "__main__":
    run(Bot().start())
