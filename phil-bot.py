import discord
import twitter
from dotenv import load_dotenv
import os
load_dotenv()


class AutoPhilled(discord.Client):
    async def on_ready(self):
        print('Here and ready to ping Phil!')
    #async def twitter update
    #   if twitter api gets followers>prev_followers and followers%5==0:
    #       send message "@everyone congratulate phil on more followers"
    #   if twitter api gets phil tweet
    #       send message "@everyone 'link to tweet'"


client = AutoPhilled()
client.run(os.getenv('PHIL_TOKEN'))