# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.


import requests
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from datetime import datetime, timedelta


# SHEETY REQUEST
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()


#MAIN
for row in sheet_data:
    flight_search = FlightSearch()
    row["iataCode"] = flight_search.get_codes(row["city"])
    flight_data = FlightData()
    now = datetime.now()
    date_from = (now + timedelta(days=1)).strftime("%d/%m/%Y")
    date_to = (now + timedelta(days=30)).strftime("%d/%m/%Y")
    return_from = (now + timedelta(days=7)).strftime("%d/%m/%Y")
    return_to = (now + timedelta(days=28)).strftime("%d/%m/%Y")
    data = flight_search.get_data(row["iataCode"], date_from, date_to, return_from, return_to)
    print(data)
    if row["lowestPrice"] > flight_data.get_prices(data):
        print(row["lowestPrice"])


