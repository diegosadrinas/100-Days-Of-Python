import requests
from datetime import datetime
from data_manager import DataManager
from pprint import pprint

APP_KEY = "0BlzBCoWWlkPcpd2nSKsc9CJkUWUJple"
APP_ID = "dsadrinasflightdealsproject"
LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/search"


class FlightSearch:
    def get_codes(self, city):
        params = {
            "apikey": APP_KEY,
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=LOCATION_ENDPOINT, params=params)
        data = response.json()
        code = data["locations"][0]["code"]
        return code

    def get_data(self, city, date_from, date_to, return_from, return_to):
        params = {
            "apikey": APP_KEY,
            "fly_from": "ATL",
            "fly_to": city,
            "date_from": date_from,
            "date_to": date_to,
            "return_from": return_from,
            "return_to": return_to,
            "flight_type": "round",
            "curr": "USD",
            "max_stopovers": 0,
            "limit": 5
        }
        response = requests.get(url=SEARCH_ENDPOINT, params=params)
        data = response.json()
        return data









