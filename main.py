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
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from init import bughunter0
SESSION_NAME = os.environ.get('SESSION_NAME', ':memory:')
DATABASE_URL = os.environ.get('DATABASE_URL')
bughunter0 = Client(
    "PyttsBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)



async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=user_id, as_copy=True)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@bughunter0.on_message(filters.command(["broadcast"]))
async def broadcast_(bot, m):
    all_users = await bot.db.get_all_users()

    broadcast_msg = m.reply_to_message

    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not bot.broadcast_ids.get(broadcast_id):
            break

    out = await m.reply_text(
        text = f"Broadcast initiated! You will be notified with log file when all the users are notified.",
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Cancel Broadcast", callback_data=f"cncl_bdct+{broadcast_id}"),
                    InlineKeyboardButton("View broadcast status", callback_data=f"sts_bdct+{broadcast_id}")
                ]
            ]
        )
    )
    start_time = time.time()
    total_users = await bot.db.total_users_count()
    done = 0
    failed = 0
    success = 0

    bot.broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )
    log_file = io.BytesIO()
    log_file.name = f'broadcast_{broadcast_id}.txt'
    broadcast_log = ''
    async for user in all_users:
        await asyncio.sleep(1)
        sts, msg = await send_msg(
            user_id = int(user['id']),
            message = broadcast_msg
        )
        if msg is not None:
            broadcast_log += msg

        if sts == 200:
            success += 1
        else:
            failed += 1

        if sts == 400:
            await bot.db.delete_user(user['id'])

        done += 1
        if bot.broadcast_ids.get(broadcast_id) is None:
            break
        else:
            bot.broadcast_ids[broadcast_id].update(
                dict(
                    current = done,
                    failed = failed,
                    success = success
                )
            )
    log_file.write(broadcast_log.encode())
    if bot.broadcast_ids.get(broadcast_id):
        bot.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))

    await asyncio.sleep(3)

    await out.delete()

    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document=log_file,
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
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
