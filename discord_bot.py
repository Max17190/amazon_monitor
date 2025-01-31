import discord
from discord import Embed
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/maxloffgren/Documents/Amazon Monitor/API.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
intents = discord.Intents.default()
client = discord.Client(intents=intents)

class BlinkMonitor:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.intents = discord.Intents.default()
        self.client = discord.Client(intents=self.intents)


    async def send_notification(self, product_data):
        embed = Embed(title='Blink Monitor',color=discord.Color.purple())
        price = product_data['offers'][0]['priceInfo']['price'] if product_data['offers'] else 'N/A'

        embed.add_field(
            name=product_data['title'],
            value=f"SKU: {product_data['asin']}\n"
            f"Price: {price}\n"
            f"Condition: New\n"
            f"Sold By: Amazon.com\n"
            f"[ATC]({product_data['link']})",
        inline=False
        )

        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)

    def run(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')

        self.client.run(self.token)