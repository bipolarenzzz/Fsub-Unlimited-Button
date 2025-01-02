# bot.py
# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import pyromod.listen
import sys
import asyncio  # Kita butuh asyncio untuk sleep
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
        """
        Inisialisasi Bot dengan parameter Pyrogram Client.
        """
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
        """
        Dipanggil saat Bot().run() memulai Pyrogram Client.
        """
        # 1) Start Pyrogram Client
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}\n——"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Berhenti. Gabung Group https://t.me/SharingUserbot untuk Bantuan"
            )
            # Jika gagal di sini, bot tidak bisa start sama sekali, wajar di-exit
            sys.exit()

        # 2) Cek FORCE_SUB (Channel Wajib Join)
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
                # Jika channel untuk FORCE_SUB tidak bisa diakses, itu fatal
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    f"Bot tidak dapat Mengambil link invite dari FORCE_SUB{key}!"
                )
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} adalah admin di Channel Tersebut, Chat ID untuk FORCE_SUB{key}: {channel_id}"
                )
                self.LOGGER(__name__).info(
                    "Bot Berhenti. Gabung Group https://t.me/SharingUserbot untuk Bantuan"
                )
                sys.exit()  # Tetap exit karena ini kondisi wajib

        # 3) Cek CHANNEL_ID Database
        try:
            # Tambahkan sedikit jeda supaya waktu (timestamp) sinkron
            await asyncio.sleep(2)

            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(
                chat_id=db_channel.id,
                text="Test Message",
                disable_notification=True
            )
            await test.delete()

            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}\n——"
            )
        except Exception as e:
            # Jika gagal kirim "Test Message", TIDAK exit agar bot tetap jalan
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username} adalah admin di Channel DataBase Anda, CHANNEL_ID Saat Ini: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot TIDAK berhenti, tapi ada error saat Test Message.\n"
                "Gabung Group https://t.me/SharingUserbot untuk Bantuan"
            )
            # sys.exit() -> Dihapus agar bot TIDAK berhenti

        # 4) Selesai inisialisasi
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"[🔥 BERHASIL DIAKTIFKAN! 🔥]\n\n"
            f"BOT Dibuat oleh @{OWNER}\n"
            f"Jika @{OWNER} Membutuhkan Bantuan, Silahkan Tanyakan di Grup https://t.me/SharingUserbot"
        )

    async def stop(self, *args):
        """
        Dipanggil saat Bot().run() dihentikan atau app dimatikan.
        """
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
