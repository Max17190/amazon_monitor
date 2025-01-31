import aiohttp
import asyncio
from track_items import asins
from dotenv import load_dotenv
import os
import discord

# load_dotenv(dotenv_path='/etc/secrets/API.env')
load_dotenv(dotenv_path='/Users/maxloffgren/Documents/Amazon Monitor/API.env')

# Private API endpoint
url = str(os.getenv('URL'))

# Discord Requirements
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
intents = discord.Intents.default()
client = discord.Client(intents=intents)

headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'test-key'
}

async def fetch_stock(session, asin):
        data = {
            'region': 'us',
            'asin': asin
        }
        try: 
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    r_json = await response.json()
                    # print(r_json)
                    in_stock = r_json['product']['inStock']
                    link = r_json['product']['link']
                    offers = r_json.get('product', {}).get('offers', [])

                    amazon_featured = any(offer.get('merchantName', '') == 'Amazon.com' for offer in offers)

                    if in_stock and amazon_featured:
                        print(f"Asin {asin} is in stock: {link}")
                        return link
                    else:
                        print(f'Asin {asin} not in stock.')
                elif response.status == 429:
                     await asyncio.sleep(1)
                     return await fetch_stock(session, asin)
                else:
                    print(f'Error occured for asin {asin}. Error Status: {response.status}')
        
        except Exception as e:
             print(f"An error occured for ASIN {asin}: {e}")

async def check_stock():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_stock(session, asin) for asin in asins]
        results = await asyncio.gather(*tasks)
        in_stock_links = [link for link in results if link is not None]

        if in_stock_links:
            print("In-stock product links:")
            for link in in_stock_links:
                print(link)
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                await channel.send(f"🚨 **Product in stock!** 🚨\n{link}")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await check_stock()
    await client.close()

# Run the bot
client.run(DISCORD_TOKEN)