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
        # 1) Mulai Pyrogram
        try:
            # (Opsional) Tambah jeda agar Dyno Heroku siap & waktu sinkron
            await asyncio.sleep(2)

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
            # Jika error saat .start(), biasanya fatal (misal token salah).
            # Namun, jika "msg_id is too low" terjadi di sini, Anda bisa pilih
            # untuk tidak menghentikan bot. Saya akan hanya menampilkan warning.
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Ada error saat .start(), tapi kita TIDAK menghentikan bot.\n"
                "Jika ini masalah 'msg_id is too low', tunggu beberapa detik atau deploy ulang.\n"
                "Jika ini masalah fatal (API_ID, token), bot mungkin tidak akan berfungsi."
            )
            # sys.exit()  # Dikomen agar bot tidak berhenti

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
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    f"Bot tidak dapat Mengambil link invite dari FORCE_SUB{key}!"
                )
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} adalah admin di Channel Tersebut, Chat ID untuk FORCE_SUB{key}: {channel_id}"
                )
                self.LOGGER(__name__).info(
                    "Bot Berhenti. Gabung Group https://t.me/SharingUserbot untuk Bantuan (Force Sub error)."
                )
                sys.exit()  # Tetap exit karena Force Sub dianggap wajib

        # 3) Cek CHANNEL_ID Database
        try:
            # Kita sudah menambah jeda sebelum super().start(),
            # jadi di sini biasanya tidak masalah. Tapi jika perlu, bisa sleep lagi.
            # await asyncio.sleep(2)

            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(
                chat_id=db_channel.id,
                text="Test Message",
                disable_notification=True
            )
            await test.delete()

            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n"
                f"┌ Title: {db_channel.title}\n"
                f"└ Chat ID: {db_channel.id}\n——"
            )

        except Exception as e:
            self.LOGGER(__name__).warning(e)
            # Tidak exit, hanya warning
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username} adalah admin di Channel DataBase Anda, CHANNEL_ID Saat Ini: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Terjadi error saat Test Message, tapi bot TIDAK berhenti.\n"
                "Jika bingung, gabung Group https://t.me/SharingUserbot untuk Bantuan."
            )
            # sys.exit() -> kita hapus agar bot tetap jalan meski test message gagal

        # 4) Selesai inisialisasi
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"[🔥 BERHASIL DIAKTIFKAN! 🔥]\n\n"
            f"BOT Dibuat oleh @{OWNER}\n"
            "Jika ada kendala, silakan tanya di Grup https://t.me/SharingUserbot"
        )

    async def stop(self, *args):
        """
        Fungsi stop() dipanggil saat Bot().run() dihentikan atau app dimatikan.
        """
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
