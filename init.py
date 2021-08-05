from collections import defaultdict
import time

from pyrogram import Client


from db.database import Database


class bughunter0(Client):

    def __init__(self):
        super().__init__(
            session_name=Config.SESSION_NAME,
            bot_token = Config.BOT_TOKEN,
            api_id = Config.API_ID,
            api_hash = Config.API_HASH,
            
            )
        

        self.db = Database(Config.DATABASE_URL, Config.SESSION_NAME)
        self.CURRENT_PROCESSES = defaultdict(lambda : 0)
        self.CHAT_FLOOD = defaultdict(lambda : int(time.time()) - Config.SLOW_SPEED_DELAY-1)
        self.broadcast_ids = {}


    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"\n\nNew session started for {me.first_name}({me.username})")


    async def stop(self):
        await super().stop()
        print('Session stopped. Bye!!')
