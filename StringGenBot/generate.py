from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**• ئەگەر دەتەوێت مۆسیقاکەت دابمەزرێنیت ئەوا بە پیرۆگرام هەڵبژێرە\n\n• ئەگەر دەتەوێت تەلەتۆن دابنێیت، تیرموکس هەڵبژێرە\n\n• وەرگیراوەکانی دانیشتن هەیە بۆ بۆتەکان**"


buttons_ques = [
    [
        InlineKeyboardButton("پیرۆگرام", callback_data="pyrogram"),
        InlineKeyboardButton("تیلیتۆن", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("پایرۆگرام بۆت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("تیلیتۆن بۆت", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text=" بۆ دەرهێنانی کۆدەکە کلیک بکە ", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "تیلیتۆن"
    else:
        ty = "پایرۆگرام"
    if is_bot:
        ty += "بۆت"
    await msg.reply(f"» ⚡ ¦ دانیشتنێک دروست بکە **{ty}** ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "باشە، بنێرە API_ID\n\nکلیک بکە /skip بەمەبەستی تەواوکردنی کۆدە کە", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**API_ID** دەبێت ژمارەیەکی تەواو بێت، دووبارە دەست بە دروستکردنی دانیشتنەکەت بکەرەوە", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "» باشە، بنێرە API_HASH", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» ✔️ ئێستا ژمارەکەت لەگەڵ کۆدی وڵاتەکەت بنێرە, نموونە :+201287585064''"
    else:
        t = "تکایە تۆکنی بۆتەکەت بنێرە بۆ بەردەوامبوون.\نموونە: `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("چاوەڕوان بن، کۆدێک بۆ ئەکاونتی تێلێگرامەکەت دەنێرین.")
    else:
        await msg.reply("» هەوڵدان بۆ چوونە ژوورەوە لە ڕێگەی بۆت تۆکن...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» هی تۆ **API_ID** و **API_HASH** تێکەڵکردن لەگەڵ سیستەمی ئەپەکانی تەلەگرامدا ناگونجێت. \n\nتکایە دەست بکە بە دروستکردنی دانیشتنەکەت", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» لە ** ژمارەی تەلەفۆن** تۆ نێردراویت سەر بە هیچ ئاکاونتیکی تەلەگرام نییە\n\nدەست بکە بە دروستکردنی دانیشتنەکەت", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "[کۆدەکە بنێرە وەک لە وێنەکەدا دیارە](https://telegra.ph/file/da1af082c6b754959ab47.jpg)» 🔍 تکایە ئەکاونتی تێلێگرامەکەت بپشکنە و کۆدەکە لە ئەکاونتی ئاگادارکردنەوەکانی تەلەگرامەکەتەوە بزانە. ئەگەر وا بووبێت\n دوو هەنگاوی پشتڕاستکردنەوە هەیە( پاسپۆرد ) ، دوای ناردنی کۆدی دەستگەیشتن بەم فۆرماتەی خوارەوە وشەی نهێنی لێرە بنێرە.-ئەگەر وشەی نهێنی یان کۆدەکە بێت\n 12345 تکایە بەم فۆرماتە بنێرن 1 2 3 4 5 لەگەڵ بۆشایی نێوان ژمارەکان ئەگەر پێویستت بە یارمەتی بوو @SARKAUT", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply(" دانیشتنەکە کاتەکەی تەواو بوو 10 خولەکە تکایە دانیشتنەکە لە سەرەتاوە دووبارە دەربهێنە .", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» ئەو otp ەی کە تۆ ناردوتە ** هەڵە.**\n\nتکایە دەست بکە بە دروستکردنی دانیشتنەکەت", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» ئەو otpی کە ناردوتە ئەوەیە ** بەسەرچوو.**\n\nتکایە دەست بکەرەوە بە دروستکردنی دانیشتنەکەت.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "وشەی نهێنی ئەکاونتەکەت بنێرە", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("کاتی دانیشتنەکە 5 خولەکه تەواو بووە، تکایە دانیشتنەکە لە سەرەتاوە دەربهێننەوە", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» ئەو وشەی نهێنیەی کە ناردووتە هەڵەیە\n\nتکایە دەست بکە بە دروستکردنی دانیشتنەکەت.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**دانیشتنەکەت {ty} String session** \n\n`{string_session}` \n\n**دروستکراوە لەلایەن :** @SARKAUT \n **تێبینی :** بیهێڵەرەوە، لای خۆت چۆنکە کەسێک دەتوانێت پێی هاکت بکات\n لێرە بەشداربە تکایە @ChanallBots"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» ✅ ️دانیشتنەکە بە سەرکەوتوویی دەرهێنرا {} .\n\n🔍تکایە بڕۆ بۆ ئەو نامانەی کە لە ئەکاونتەکەتدا سەیڤ کراون!  ! \n\n**بۆتێکی مۆلیدەی ڕیز لەلایەن** @SARKAUT ".format("تیلیتۆن" if telethon else "پیرۆگرام"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("** داواکاریەکەت تەواو بوو پرۆسەکە تەواو بوو بۆ دەستپێکردن بنووسە /start !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» دووبارە دەستی پێکردووەتەوە  !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» پرۆسەی درووستکردنی ڕستەی بەردەوامی گەنسڵ کرد !**", quote=True)
        return True
    else:
        return False
