import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_DISCORD = os.getenv('TOKEN_DISCORD')
TOKEN_LINE_NOTIFY = os.getenv('TOKEN_LINE_NOTIFY')

intents = discord.Intents.default()
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel_name = after.channel.name
        message = f'{member.display_name} joined a voice channel {channel_name}!'
        send_line_notify(message)
    elif before.channel is not None and after.channel is None:
        channel_name = before.channel.name
        message = f'{member.display_name} left a voice channel {channel_name}!'
        send_line_notify(message)

def send_line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {TOKEN_LINE_NOTIFY}'}
    data = {'message': message}
    requests.post(url, headers=headers, data=data)

client.run(TOKEN_DISCORD)

