import requests

def get_place_coordinates(api_key, input_text):
    endpoint = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        'input': input_text,
        'types': 'geocode',
        'key': api_key,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    predictions = data.get('predictions', [])
    return predictions
