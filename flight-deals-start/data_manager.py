import requests

SHEETY_USER = "dsadrinas"
SHEETY_PASS = "flightdealspass"
SHEETY_ENDPOINT = "https://api.sheety.co/929474b28794ea4224e4e966b4706d83/flightDeals/prices"
SHEETY_HEADER = {
            "Authorization": "Basic ZHNhZHJpbmFzOmZsaWdodGRlYWxzcGFzcw=="
        }


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
