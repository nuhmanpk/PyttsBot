# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import logging
import pyrogram
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
from gtts import gTTS 
import db.database as sql


bughunter0 = Client(
    "PyttsBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_STR = """
Hi **{}**, I'm PyTTs Bot. I can convert text into speech
"""
ABOUT = """
**BOT:** `PYTTS BOT`
**AUTHOR :** [bughunter0](https://t.me/bughunter0)
**SERVER :** `Heroku`
**LIBRARY :** `Pyrogram`
**SOURCE :** [BugHunterBots](https://t.me/bughunterbots)
**LANGUAGE :** `Python 3.9`
"""
HELP = """
Send / Forward me a text / message to convert it to Speech\n Or Send me an emoji to Return it as Speech
"""
START_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('ABOUT',callback_data='cbabout'),
        InlineKeyboardButton('HELP',callback_data='cbhelp')
        ],
        [
        InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/BughunterBots'),
        ]]
        
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back',callback_data='cbclose'),
        ]]
    )

@bughunter0.on_message(filters.command(["broadcast"]))
async def broadcast (bot,message):
    to_send = message.reply_to_message.text.split(None, 1)
    if len(to_send) >= 2:
        chats = sql.get_all_chats() or []
        failed = 0
        for chat in chats:
            try:
                chat_id = chat.chat_id
                bot.sendMessage(chat_id=chat_id, text=to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                await message.reply_text("Couldn't send broadcast to %s, group name %s", str(chat.chat_id), str(chat.chat_name))

        await message.reply_text("Broadcast complete. {} groups failed to receive the message, probably "
                                            "due to being kicked.".format(failed))

 


@bughunter0.on_callback_query() # callbackQuery()
async def cb_data(bot, update):  
    if update.data == "cbhelp":
        await update.message.edit_text(
            text=HELP,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data == "cbabout":
        await update.message.edit_text(
            text=ABOUT,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    else:
        await update.message.edit_text(
            text=START_STR.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )

@bughunter0.on_message(filters.command(["start"])) # StartCommand
async def start(bot, update):
     await update.reply_text(
        text=START_STR.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTON
    )

@bughunter0.on_message((filters.text | filters.forwarded | filters.reply) & filters.private)
async def tts(bot, message):
  try:
       if message.text:
          chat_id = int(message.chat.id)
          text = str(message.text)
          tx = await bot.send_message(text="Converting to Speech...",chat_id=chat_id)
        # change Language from here
          language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                              # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
          tts_file = gTTS(text=text, lang=language, slow=False) 
          tts_file.save(f"{message.chat.id}.mp3") 
          with open(f"{message.chat.id}.mp3", "rb") as speech:
                await bot.send_voice(chat_id, speech, caption ="@BugHunterBots")
          await tx.delete()
       else:
          await message.reply_text("I can't find Text in this message")
  except Exception as error:
       print (error)
       await message.reply_text("Oops Something Bad occurred!!")



bughunter0.run()
