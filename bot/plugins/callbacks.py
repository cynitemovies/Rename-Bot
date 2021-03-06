# (c) @CyniteOfficial

from pyrogram import types
from bot.client import Client
from bot.core.db.database import db
from bot.core.file_info import (
    get_media_file_name,
    get_media_file_size,
    get_file_type,
    get_file_attr
)
from bot.core.display import humanbytes
from bot.core.handlers.settings import show_settings


@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    if cb.data == "showSettings":
        await cb.answer()
        await show_settings(cb.message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if not thumbnail:
            await cb.answer("ππΎπ π³πΈπ³π½'π ππ΄π π°π½π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ»!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(cb.message.chat.id, thumbnail, "π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ»",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("π³π΄π»π΄ππ΄ ππ·ππΌπ±π½π°πΈπ»",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(cb.from_user.id, None)
        await cb.answer("πΎπΊπ°π, πΈ π³π΄π»π΄ππ΄π³ ππΎππ π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ». π½πΎπ πΈ ππΈπ»π» π°πΏπΏπ»π π³π΄π΅π°ππ»π ππ·ππΌπ±π½π°πΈπ».", show_alert=True)
        await cb.message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer()
        await cb.message.edit("ππ΄π½π³ πΌπ΄ π°π½π πΏπ·πΎππΎ ππΎ ππ΄π ππ·π°π π°π π²ππππΎπΌ ππ·ππΌπ±π½π°πΈπ».\n\n"
                              "πΏππ΄ππ /cancel ππΎ π²π°π½π²π΄π» πΏππΎπ²π΄ππ..")
        from_user_thumb: "types.Message" = await c.listen(cb.message.chat.id)
        if not from_user_thumb.photo:
            await cb.message.edit("<b>πΏππΎπ²π΄ππ π²π°π½π²π΄π»π»π΄π³</b>")
            return await from_user_thumb.continue_propagation()
        else:
            await db.set_thumbnail(cb.from_user.id, from_user_thumb.photo.file_id)
            await cb.message.edit("πΎπΊπ°π!\n"
                                  "π½πΎπ πΈ ππΈπ»π» π°πΏπΏπ»π ππ·πΈπ ππ·ππΌπ±π½π°πΈπ» ππΎ π½π΄ππ ππΏπ»πΎπ°π³π.",
                                  reply_markup=types.InlineKeyboardMarkup(
                                      [[types.InlineKeyboardButton("π±πΎπ ππ΄πππΈπ½πΆπ",
                                                                   callback_data="showSettings")]]
                                  ))
    elif cb.data == "setCustomCaption":
        await cb.answer()
        await cb.message.edit("Okay,\n"
                              "ππ΄π½π³ πΌπ΄ ππΎππ π²ππππΎπΌ π²π°πΏππΈπΎπ½.\n\n"
                              "πΏππ΄ππ /cancel ππΎ π²π°π½π²π΄π» πΏππΎπ²π΄ππ..")
        user_input_msg: "types.Message" = await c.listen(cb.message.chat.id)
        if not user_input_msg.text:
            await cb.message.edit("<b>πΏππΎπ²π΄ππ π²π°π½π²π΄π»π»π΄π³</b>")
            return await user_input_msg.continue_propagation()
        if user_input_msg.text and user_input_msg.text.startswith("/"):
            await cb.message.edit("<b>πΏππΎπ²π΄ππ π²π°π½π²π΄π»π»π΄π³</b>")
            return await user_input_msg.continue_propagation()
        await db.set_caption(cb.from_user.id, user_input_msg.text.markdown)
        await cb.message.edit("π²ππππΎπΌ π²π°πΏππΈπΎπ½ π°π³π³π΄π³ πππ²π²π΄πππ΅ππ»π»π!",
                              reply_markup=types.InlineKeyboardMarkup(
                                  [[types.InlineKeyboardButton("π±πΎπ ππ΄πππΈπ½πΆπ",
                                                               callback_data="showSettings")]]
                              ))
    elif cb.data == "triggerApplyCaption":
        await cb.answer()
        apply_caption = await db.get_apply_caption(cb.from_user.id)
        if not apply_caption:
            await db.set_apply_caption(cb.from_user.id, True)
        else:
            await db.set_apply_caption(cb.from_user.id, False)
        await show_settings(cb.message)
    elif cb.data == "triggerApplyDefaultCaption":
        await db.set_caption(cb.from_user.id, None)
        await cb.answer("πΎπΊπ°π, π½πΎπ πΈ ππΈπ»π» πΊπ΄π΄πΏ π³π΄π΅π°ππ»π π²π°πΏππΈπΎπ½.", show_alert=True)
        await show_settings(cb.message)
    elif cb.data == "showCaption":
        caption = await db.get_caption(cb.from_user.id)
        if not caption:
            await cb.answer("ππΎπ π³πΈπ³π½'π ππ΄π π°π½π π²ππππΎπΌ π²π°πΏππΈπΎπ½!", show_alert=True)
        else:
            await cb.answer()
            await cb.message.edit(
                text=caption,
                parse_mode="Markdown",
                reply_markup=types.InlineKeyboardMarkup([[
                    types.InlineKeyboardButton("π±π°π²πΊ", callback_data="showSettings")
                ]])
            )
    elif cb.data == "triggerUploadMode":
        await cb.answer()
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(cb.from_user.id, False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, True)
        await show_settings(cb.message)
    elif cb.data == "showFileInfo":
        replied_m = cb.message.reply_to_message
        _file_name = get_media_file_name(replied_m)
        text = f"**π΅πΈπ»π΄ π½π°πΌπ΄ :** `{_file_name}`\n\n" \
               f"**π΅πΈπ»π΄ π΄πππ΄π½ππΈπΎπ½ :** `{_file_name.rsplit('.', 1)[-1].upper()}`\n\n" \
               f"**π΅πΈπ»π΄ πππΏπ΄ :** `{get_file_type(replied_m).upper()}`\n\n" \
               f"**π΅πΈπ»π΄ ππΈππ΄ :** `{humanbytes(get_media_file_size(replied_m))}`\n\n" \
               f"**π΅πΈπ»π΄ π΅πΎππΌπ°π :** `{get_file_attr(replied_m).mime_type}`"
        await cb.message.edit(
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("π²π»πΎππ΄", callback_data="closeMessage")]]
            )
        )
    elif cb.data == "closeMessage":
        await cb.message.delete(True)
