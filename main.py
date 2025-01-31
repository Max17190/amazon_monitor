import aiohttp
import asyncio
from track_items import asins
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/maxloffgren/Documents/Amazon Monitor/API.env')

# Private API endpoint
url = str(os.getenv('URL'))

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
                    offers = r_json.get('offers', [])

                    amazon_featured = any(
                    offer.get('seller', '') == 'Amazon.com'
                    for offer in offers
                    )

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