# bot.py
# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import pyromod.listen
import sys
import asyncio
from pyrogram import Client, enums
from config import (
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    FORCE_SUB,
    LOGGER,
    OWNER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        # 1) Mulai Pyrogram
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n"
                f"┌ First Name: {self.namebot}\n"
                f"└ Username: @{self.username}\n——"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Berhenti. Gabung Group https://t.me/SharingUserbot untuk Bantuan (Error on .start())"
            )
            sys.exit()  # Kalau gagal .start() di awal, wajar bot exit

        # 2) Cek FORCE_SUB
        for key, channel_id in FORCE_SUB.items():
            try:
                info = await self.get_chat(channel_id)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(channel_id)
                    link = info.invite_link
                setattr(self, f"invitelink{key}", link)
                self.LOGGER(__name__).info(
                    f"FORCE_SUB{key} detected!\n┌ Title: {info.title}\n└ Chat ID: {info.id}\n——"
                )
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    f"Bot tidak dapat Mengambil link invite dari FORCE_SUB{key}!"
                )
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} adalah admin di Channel Tersebut, Chat ID: {channel_id}"
                )
                self.LOGGER(__name__).info(
                    "Bot Berhenti. Gabung Group https://t.me/SharingUserbot untuk Bantuan (Force Sub error)"
                )
                sys.exit()

        # 3) Cek CHANNEL_ID Database
        try:
            # Beri jeda agar sinkronisasi waktu (timestamp) sempat jalan
            await asyncio.sleep(2)

            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
            await test.delete()

            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}\n——"
            )

        except Exception as e:
            self.LOGGER(__name__).warning(e)
            # HANYA peringatan. TIDAK exit.
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username} adalah admin di Channel: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Terjadi error saat Test Message, tapi bot TIDAK berhenti.\n"
                "Jika bingung, gabung Group https://t.me/SharingUserbot untuk Bantuan."
            )
            # DULU: sys.exit() -> dihapus agar bot tidak mati

        # 4) Selesai start
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"[🔥 BERHASIL DIAKTIFKAN! 🔥]\n\n"
            f"BOT Dibuat oleh @{OWNER}\n"
            "Jika ada kendala, silakan tanya di Grup https://t.me/SharingUserbot"
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
