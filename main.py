from discord_bot import BlinkMonitor
from monitor import StockMonitor
from track_items import asins
from dotenv import load_dotenv
import os
import asyncio
import aiohttp

class Application:
    def __init__(self):
        load_dotenv()
        self.monitor = StockMonitor(
            url=os.getenv('URL'),
            headers={
                'Content-Type': 'application/json',
                'x-api-key': 'test-key'
            }
        )
        self.discord_bot = BlinkMonitor(
            token=os.getenv('DISCORD_TOKEN'),
            channel_id=int(os.getenv('DISCORD_CHANNEL_ID'))
        )

    async def run_monitor(self):
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.monitor.fetch_stock(session, asin) for asin in asins]
                results = await asyncio.gather(*tasks)
                for product in results:
                    if product:
                        await self.discord_bot.send_notification(product)
                await asyncio.sleep(30)

if __name__ == "__main__":
    app = Application()
    app.discord_bot.run()
