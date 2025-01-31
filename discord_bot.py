import discord
from discord import Embed

class BlinkMonitor:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.intents = discord.Intents.default()
        self.client = discord.Client(intentself.intents)

    async def send_notification(self, product_data):
        embed = Embed(title='Blink Monitor',color=discord.Color.purple())
        embed.add_field(
            name = product_data['title'],
            value=f"SKU: {product_data['asin']}\n"
                  f"Price: {product_data['price']}\n"
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