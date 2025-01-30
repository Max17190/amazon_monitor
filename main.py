import requests

url = 'https://api.enven.io/v1/products'

headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'test-key'
}

data = {
    'region': 'us',
    'asin': 'whatever'
}


r = requests.post(url, json=data, headers=headers)

print("Status Code:", r.status_code)
print("Response Body:", r.json())

