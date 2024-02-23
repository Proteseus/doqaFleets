import requests

def find_coordinates(location):
    url = "https://autocomplete.search.hereapi.com/v1/geocode"
    params = {
        'q': location,
        'in': 'countryCode:ETH',
        'qq': 'city=Addis Ababa',
        'lang': 'en-US',
        'limit': 1,
        'apiKey': 'mS2xA92lRv89XGpbQlxp5znBgCHdi6u-zOf-Ttecheo'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['items']) >= 1:
            result = {'result': [data['items'][0]['position']['lng'], data['items'][0]['position']['lat']]}
            print(result)
            return result
        else:
            print('not found')
            return {'result': 'Not found'}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {'status': response.status_code, 'message': response.text}

