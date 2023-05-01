from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""• بەخێربێیت بەڕێز 

• دەتوانن ئەمانەی خوارەوە دەربهێنن

• تێلیتۆنی تێرموکس بۆ ئەکاونتەکان

• تێرمیکس تێلێتۆن بۆ بۆتەکان

• پایرۆگرام میوزیک بۆ ئەکاونتەکان

• پایرۆگرام میوزیک بۆ بۆتەکان
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="بۆ دەرهێنانی کۆدەکە کلیک بکە", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("جە ناڵ بۆت", url="https://t.me/ChanallBots"),
                    InlineKeyboardButton("خاوە ن بۆت", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
