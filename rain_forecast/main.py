import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

API_KEY = "53a7475fbd4058c735019c2bfa2f1cf8"
ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "AC9cdffe39b2b870f905335be929302ef5"
auth_token = "05bc1669a7e9030e30550a423ffd5643"


weather_params = {
    "lat": -34.603683,
    "lon": -58.381557,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"

}

response = requests.get(url=ENDPOINT, params=weather_params)

response.raise_for_status()
weather_data = response.json()
twelve_hour_weather = weather_data["hourly"][:12]
condition_codes = [hour["weather"][0]["id"] for hour in twelve_hour_weather]

will_rain = False
for i in condition_codes:
    if i < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ.get('https_proxy')}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Today's gonna rain! 🌧",
        from_='+12183767080',
        to='+541157095128'
    )





