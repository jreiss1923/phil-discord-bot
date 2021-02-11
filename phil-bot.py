import discord
from dotenv import load_dotenv
import os
load_dotenv()


class AutoPhilled(discord.Client):
    async def on_ready(self):
        print('Here and ready to ping Phil!')


client = AutoPhilled()
client.run(os.getenv('PHIL_TOKEN'))