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
                print(f"Response status for ASIN {asin}: {response.status}")

                # Out of stock handler
                if response.status == 200:
                    r_json = await response.json()
                    product = r_json.get('product', {})
                    if self._is_valid_stock(r_json):
                        print(f"ASIN {asin}: In Stock")
                    else:
                        print(f"ASIN {asin}: Out of Stock")
                    return product if self._is_valid_stock(r_json) else None
                
                # Rate limit handler
                elif response.status == 429:
                    print(f"Rate limited for ASIN {asin}. Retrying after 1 second...")
                    await asyncio.sleep(1)
                    return await self.fetch_stock(session, asin)
                
        except Exception as e:
            print(f"Error monitoring ASIN {asin}: {e}")
            return None

    # Check in stock and seller
    def _is_valid_stock(self, r_json):
        product = r_json.get('product', {})
        offers = product.get('offers', [])
        return (
            product.get('inStock', False) and
            any(
                (offer.get('merchantName') in ('Amazon.com', '') or not offer.get('merchantName')) and
                float(offer.get('priceInfo', {}).get('price', '0')) > 0
                for offer in offers
            )
        )