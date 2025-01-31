import discord
from discord import Embed
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/maxloffgren/Documents/Amazon Monitor/API.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

class BlinkMonitor:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.intents = discord.Intents.default()
        self.client = discord.Client(intents=self.intents)
        self.channel = None

    async def send_notification(self, product_data):
        if not self.channel:
            self.channel = self.client.get_channel(self.channel_id)
            if not self.channel:
                print(f"Error: Channel with ID {self.channel_id} not found.")
                return

        embed = Embed(title='Blink Monitor', color=discord.Color.purple())
        price = product_data['offers'][0]['priceInfo']['price'] if product_data['offers'] else 'N/A'

        embed.add_field(
            name=product_data['title'],
            value=f"""
            **SKU:** {product_data['asin']}

            **Price:** {price}

            **Condition:** New

            **Sold By:** Amazon.com

            [VIEW PRODUCT]({product_data['link']})
            """,
            inline=False
        )


        await self.channel.send(embed=embed)

    def run(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')
            self.channel = self.client.get_channel(self.channel_id)
            if not self.channel:
                print(f"Error: Channel with ID {self.channel_id} not found.")

        self.client.run(self.token)