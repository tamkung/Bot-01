import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_DISCORD = os.getenv('TOKEN_DISCORD')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')  # ใช้ Webhook URL

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
        message = f'🔊 {member.display_name} : joined the voice channel **{channel_name}**!'
        send_discord_webhook(message)
    elif before.channel is not None and after.channel is None:
        channel_name = before.channel.name
        message = f'🔇 {member.display_name} : left the voice channel **{channel_name}**!'
        send_discord_webhook(message)

def send_discord_webhook(message):
    url = DISCORD_WEBHOOK_URL  # ใช้ Webhook URL
    data = {'content': message}  # Discord Webhook ใช้ key 'content'
    response = requests.post(url, json=data)

    if response.status_code != 204:
        print(f"❌ Failed to send message: {response.status_code} - {response.text}")

client.run(TOKEN_DISCORD)
