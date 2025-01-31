from discord_bot import BlinkMonitor
from monitor import StockMonitor
from track_items import asins
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import signal

load_dotenv(dotenv_path='/Users/maxloffgren/Documents/Amazon Monitor/API.env')

class Application:
    def __init__(self):
        load_dotenv()
        self.monitor = StockMonitor(
            url = str(os.getenv('URL')),
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': 'test-key'
            }
        )
        self.discord_bot = BlinkMonitor(
            token = os.getenv('DISCORD_TOKEN'),
            channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        )
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)    
        self.shutdown = False

    async def run_monitor(self):
        async with aiohttp.ClientSession() as session:
            while not self.shutdown:
                for asin in asins:
                    product = await self.monitor.fetch_stock(session, asin)
                    if product:
                        await self.discord_bot.send_notification(product)

                    # Request Delay    
                    await asyncio.sleep(1)

                # 5 Second Sleep Cycle    
                await asyncio.sleep(5)

    def handle_shutdown(self, signal, frame):
        print("Shutting down gracefully...")
        self.shutdown = True
        self.loop.create_task(self.discord_bot.client.close())
        self.loop.stop()

if __name__ == "__main__":
    app = Application()

    signal.signal(signal.SIGINT, app.handle_shutdown)
    signal.signal(signal.SIGTERM, app.handle_shutdown)

    try:
        app.loop.create_task(app.run_monitor())
        app.loop.run_until_complete(app.discord_bot.client.start(app.discord_bot.token))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if not app.loop.is_closed():
            app.loop.close()