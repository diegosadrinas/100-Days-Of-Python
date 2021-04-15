import requests

account_sid = "AC9cdffe39b2b870f905335be929302ef5"
auth_token = "05bc1669a7e9030e30550a423ffd5643"
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os


class NotificationManager():
    # This class is responsible for sending notifications with the deal flight details.
    def send_sms(self, data):
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ.get('https_proxy')}
        client = Client(account_sid, auth_token, http_client=proxy_client)
        message = client.messages \
            .create(
                body="",
                from_='+12183767080',
                to='+541157095128'
        )
