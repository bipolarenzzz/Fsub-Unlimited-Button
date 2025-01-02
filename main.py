import os
from asyncio import run
from pyrogram import Client

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="my_bot",
            # Dibaca dari environment variable Heroku
            api_id=int(os.environ["APP_ID"]),
            api_hash=os.environ["API_HASH"],
            bot_token=os.environ["TG_BOT_TOKEN"],
        )

if __name__ == "__main__":
    run(Bot().start())
