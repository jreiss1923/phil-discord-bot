import discord
import datetime
from twitter import api
from dotenv import load_dotenv
import os

load_dotenv()

client = discord.Client()

twitter_api = api.Api(consumer_key=os.getenv('TWITTER_API_TOKEN'),
                      consumer_secret=os.getenv('TWITTER_API_SECRET_TOKEN'),
                      access_token_key=os.getenv('TWITTER_ACCESS_TOKEN'),
                      access_token_secret=os.getenv('TWITTER_ACCESS_SECRET_TOKEN'))

last_phil_tweet_date = None
phil_follower_count = 0


# converts Twitter time str to datetime
def convert_str_to_date(tweet_time_arr):
    tweet_time_arr = tweet_time_arr.split()
    year = int(tweet_time_arr[5])
    month = convert_month_code(tweet_time_arr[1])
    day = int(tweet_time_arr[2])
    hour = int(tweet_time_arr[3][0:2])
    minute = int(tweet_time_arr[3][3:5])
    second = int(tweet_time_arr[3][6:8])

    return datetime.datetime(year, month, day, hour, minute, second)


# converts the month code in Twitter date to month num
def convert_month_code(month_str):
    if month_str == 'Jan':
        return 1
    elif month_str == 'Feb':
        return 2
    elif month_str == 'Mar':
        return 3
    elif month_str == 'Apr':
        return 4
    elif month_str == 'May':
        return 5
    elif month_str == 'Jun':
        return 6
    elif month_str == 'Jul':
        return 7
    elif month_str == 'Aug':
        return 8
    elif month_str == 'Sep':
        return 9
    elif month_str == 'Oct':
        return 10
    elif month_str == 'Nov':
        return 11
    elif month_str == 'Dec':
        return 12


# Sends Phil twitter updates and Phil follower counts to the specified channel
@client.event
async def phil_twitter_update(self):
    global phil_follower_count
    global last_phil_tweet_date
    await client.wait_until_ready()

    while True:
        # current channel: Test - general
        channel = client.get_channel(458644594905710595)

        # gets timeline, profile of Phil
        phil_timeline = twitter_api.GetUserTimeline(screen_name="Weeabuddhaboo")
        phil_twitter_followers = int(twitter_api.GetUser(screen_name="Weeabuddhaboo").AsDict()['followers_count'])

        # gets most recent status and posts if not a retweet
        for status in phil_timeline:
            status_dict = status.AsDict()
            if not status_dict.keys().__contains__('retweeted_status') and (
                    last_phil_tweet_date is None or last_phil_tweet_date < convert_str_to_date(status_dict['created_at'])):
                await channel.send("@everyone https://twitter.com/Weeabuddhaboo/status/" + str(status_dict['id']))
                last_phil_tweet_date = convert_str_to_date(status_dict['created_at'])
                break

        # gets follower count and sends congratulations message
        if phil_twitter_followers > phil_follower_count and phil_twitter_followers % 5 == 0:
            await channel.send("@everyone congratulate Phil on reaching " + str(phil_twitter_followers) + " followers!")

        # make sure to update the follower count
        phil_follower_count = phil_twitter_followers


client.loop.create_task(phil_twitter_update(client))
client.run(os.getenv('PHIL_BOT_TOKEN'))
