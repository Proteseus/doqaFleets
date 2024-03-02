import requests
import polyline
import folium

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
    res = r.json()   
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }

    return out

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
            result = {'result': [data['items'][0]['title'], data['items'][0]['position']['lat'], data['items'][0]['position']['lng']]}
            print(result)
            return result
        else:
            print('not found')
            return {'result': 'Not found'}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {'status': response.status_code, 'message': response.text}

def find_address(location):
    url = "https://revgeocode.search.hereapi.com/v1/revgeocode"
    params = {
        'in': f'circle:{location};r=2000',
        'types': 'city',
        'lang': 'en-US',
        'limit': 1,
        'apiKey': 'mS2xA92lRv89XGpbQlxp5znBgCHdi6u-zOf-Ttecheo'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['items']) >= 1:
            result = {'result': [data['items'][0]['title'], data['items'][0]['position']['lat'], data['items'][0]['position']['lng']]}
            print(result)
            return result
        else:
            print(f'not found for {location}')
            return {'result': 'Not found'}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {'status': response.status_code, 'message': response.text}


def find_city(location):
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        'q': location,
        'in': 'countryCode:ETH',
        'lang': 'en-US',
        'limit': 1,
        'apiKey': 'mS2xA92lRv89XGpbQlxp5znBgCHdi6u-zOf-Ttecheo'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['items']) >= 1:
            result = {'result': [data['items'][0]['title'], data['items'][0]['position']['lat'], data['items'][0]['position']['lng']]}
            print(result)
            return result
        else:
            print('not found')
            return {'result': 'Not found'}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {'status': response.status_code, 'message': response.text}

