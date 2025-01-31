import aiohttp
import asyncio
from track_items import asins

url = 'https://api.enven.io/v1/products'

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
                    in_stock = r_json['product']['inStock']
                    link = r_json['product']['link']

                    if in_stock:
                        print(f"Asin {asin} is in stock: {link}")
                        return link
                    else:
                        print(f'Failed to fetch data for ASIN {asin}. Status: {response.status}')
        
        except Exception as e:
             print(f"An error occured for ASIN {asin}: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_stock(session, asin) for asin in asins]
        results = await asyncio.gather(*tasks)
        in_stock_links = [link for link in results if link is not None]

        if in_stock_links:
             print("In-stock product links:")
             for link in in_stock_links:
                  print(link)

asyncio.run(main())