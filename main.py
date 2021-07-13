# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
from gtts import gTTS 
from pyrogram.types import ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)



    
bughunter0 = Client(
    "PyttsBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)



@bughunter0.on_message(filters.command(["test"])
def start(bot, message):
   member = int(message.chat.id)
   for member in bughunter0.iter_chat_members("BugHunterBots"):
       print (member.user.first_name)
   await message.reply_text("Sent me the Text, Then Reply /pytts to the message!! \n @BughunterBots")
  

@bughunter0.on_message(filters.command(["pytts"]))
async def tts(bot, message):
  try:
      if message.reply_to_message is None:
            await message.reply_text("Please use /pytts as a Reply to a Text")
      else :
            if message.reply_to_message.text:
                  text = str(message.reply_to_message.text)
                # change Language from here
                  language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                                      # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
                  tts_file = gTTS(text=text, lang=language, slow=False) 
                  tts_file.save(f"{message.chat.id}.mp3") 
                  chat_id = str(message.chat.id)
                  with open(f"{message.chat.id}.mp3", "rb") as speech:
                          await bot.send_voice(chat_id, speech, caption ="@BugHunterBots")
            else:
                  await message.reply_text("Ouch !! I can't find Text in this message")
  except Exception as error:
       print (error)
       await message.reply_text("Oops Something Bad occurred!!")

bughunter0.run()
