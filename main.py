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
    
bughunter0 = Client(
    "PyttsBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, message):
   await message.reply_text("Hi, Sent Me a The message for Converting to Speech \n\n @BughunterBots")

@bughunter0.on_message((filters.text | filters.forwarded | filters.reply) & filters.private)
async def tts(bot, message):
  try:
       if message.text:
          text = str(message.text)
        # change Language from here
          language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                              # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
          tts_file = gTTS(text=text, lang=language, slow=False) 
          tts_file.save(f"{message.chat.id}.mp3") 
          chat_id = int(message.chat.id)
          tx = await bot.send_message(text="Converting to Voice...",chat_id=chat_id)
          with open(f"{message.chat.id}.mp3", "rb") as speech:
                await bot.send_voice(chat_id, speech, caption ="@BugHunterBots")
          await tx.delete()
       else:
          await message.reply_text("Ouch !! I can't find Text in this message")
  except Exception as error:
       print (error)
       await message.reply_text("Oops Something Bad occurred!!")

bughunter0.run()
