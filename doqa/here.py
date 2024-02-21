import requests
from pprint import pprint

url = "https://autocomplete.search.hereapi.com/v1/geocode"
params = {
    'q': 'vibes hotel, addis ababa',
    'in': 'countryCode:ETH',
    'lang': 'en-US',
    'limit': 1,
    'apiKey': 'mS2xA92lRv89XGpbQlxp5znBgCHdi6u-zOf-Ttecheo'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    # Process the response content here
    data = response.json()
    pprint(data['items'][0]['position'], indent=4)
else:
    print(f"Error: {response.status_code}, {response.text}")
