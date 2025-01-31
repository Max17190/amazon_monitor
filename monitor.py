import aiohttp
import asyncio

class StockMonitor:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    async def fetch_stock(self, session, asin):
        data = {
            'region': 'us',
            'asin': asin
        }
        
        try:
            async with session.post(self.url, json=data, headers=self.headers) as response:
                if response.status == 200:
                    r_json = await response.json()
                    return r_json['product'] if self._is_valid_stock(r_json) else None
                elif response.status == 429:
                    await asyncio.sleep(1)
                    return await self.fetch_stock(session, asin)
        except Exception as e:
            print(f"Error monitoring ASIN {asin}: {e}")
            return None

    def _is_valid_stock(self, r_json):
        product = r_json.get('product', {})
        offers = product.get('offers', [])
        return (
            product.get('inStock') and 
            any(offer.get('merchantName') == 'Amazon.com' for offer in offers)
        )