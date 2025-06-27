from ChannelCheck.settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio


async def is_live(channel_name: str) -> bool:
    twitch = await Twitch(TWITCH_CLIENT_ID,TWITCH_CLIENT_SECRET)
    user = await first(twitch.get_users(logins=channel_name))
    stream = await first(twitch.get_streams(user_id=[user.id]))
    if stream:
        return "online"
    return "offline"
