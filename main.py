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
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)



    
bughunter0 = Client(
    "PyttsBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@bughunter0.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "{}, you are **not subscribed** to my [channel](https://t.me/{}) yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("UnMute Me", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **I am not an admin in @{channel}**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
        client.leave_chat(chat_id)


@bughunter0.on_message(filters.command(["start"]))
async def start(bot, message):
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
