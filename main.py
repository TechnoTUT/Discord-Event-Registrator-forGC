import discord
from client import Client
import os
import dotenv

dotenv.load_dotenv()


intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.messages = True

client = Client(intents=intents)
client.run(token=os.getenv("DISCORD_TOKEN"))
