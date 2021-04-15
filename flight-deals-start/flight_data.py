import requests


class FlightData:

    def get_prices(self, data):
        price = data["data"][0]["price"]
        city = data["data"][0]['cityTo']
        print(f"{city}:{price}")
        return price

    def get_sms_info(self, data):
        price = data["data"][0]["price"]
        city_from = city = data["data"][0]['cityFrom']
        departure_iata_code = data["data"][0]['flyFrom']
        arrival_city_code = data["data"][0]['cityTo']
        arrival_iata_code = data["data"][0]['flyTo']
        pass