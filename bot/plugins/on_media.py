# (c) @CyniteOfficial

import asyncio
from bot.client import Client
from bot.core.db.add import (
    add_user_to_database
)
from pyrogram import (
    filters,
    types
)


@Client.on_message((filters.video | filters.audio | filters.document) & ~filters.channel)
async def on_media_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await asyncio.sleep(3)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="**<b>ππ·πΎππ»π³ πΈ ππ·πΎπ π΅πΈπ»π΄ πΈπ½π΅πΎππΌπ°ππΈπΎπ½..?</b>**",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("ππ΄π", callback_data="showFileInfo"),
              types.InlineKeyboardButton("π½πΎ", callback_data="closeMessage")]]
        ),
        disable_web_page_preview=True,
        reply_to_message_id=m.message_id
    )
