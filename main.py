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
    "Pyrogram-tts-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, message):
   await message.reply_text("ചത്തൊന്ന് അറിയാൻ വന്നതാ ല്ലേ.... !!")

@bughunter0.on_message(filters.command(["tts"]))
async def tts(bot, message):
  try:
      text = str(message.reply_to_message.text)
      language = 'en-in'
      tts_file = gTTS(text=text, lang=language, slow=False) 
      tts_file.save(f"{message.chat.id}.mp3") 
      chat_id = str(message.chat.id)
      with open(f"{message.chat.id}.mp3", "rb") as speech:
           await bot.send_audio(chat_id, speech, progress=progress)
      os.remove(tts_file)
  except Exception as error:
       print (error)

bughunter0.run()
