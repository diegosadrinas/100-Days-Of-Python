import requests
from datetime import date, timedelta
from dotenv import dotenv_values
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

config = dotenv_values(".env")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = config["STOCK_API"]
NEWS_API = config["NEWS_API"]
TWILLIO_ID = config["TWILLIO_ID"]
TWILLIO_TOKEN = config["TWILLIO_TOKEN"]


def get_dates(string):
    today = date.today()
    today_name = today.strftime("%A")
    yesterday = today - timedelta(days=1)
    before_yesterday = today - timedelta(days=2)

    if today_name == "Monday":
        yesterday = today - timedelta(days=3)
        before_yesterday = today - timedelta(days=2)
    elif today_name == "Tuesday":
        yesterday = today - timedelta(days=1)
        before_yesterday = today - timedelta(days=4)
    if string == "today":
        return today
    elif string == "yesterday":
        return yesterday
    elif string == "before":
        return before_yesterday


def sms_body(variation, news_dict, number):
    first_three_titles = [news_dict["articles"][i]["title"] for i in range(3)]
    first_three_news = [news_dict["articles"][i]["description"] for i in range(3)]
    sms_percent = None
    if variation > 0:
        sms_percent = f"🔺{variation}%"
    elif variation < 0:
        sms_percent = f"🔻{abs(variation)}%"
    sms_title = f"{COMPANY_NAME}: {sms_percent}"
    sms_headline = f"Headline: {first_three_titles[number]}"
    sms_brief = f"Brief: {first_three_news[number]}"
    sms_final = f"{sms_title}\n{sms_headline}\n{sms_brief}"
    return sms_final


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API
}

stock_response = requests.get(url="https://www.alphavantage.co/query?", params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()

today = get_dates("today")
yesterday = get_dates("yesterday")
before_yesterday = get_dates("before")

stock_price_yesterday = float(stock_data["Time Series (Daily)"][str(yesterday)]["4. close"])
stock_price_before = float(stock_data["Time Series (Daily)"][str(before_yesterday)]["4. close"])

news_params = {
    "q": COMPANY_NAME,
    "qInTitle": COMPANY_NAME,
    "from": get_dates("yesterday"),
    "to": get_dates("today"),
    "language": "en",
    "sortBy": "relevancy",
    "apiKey": NEWS_API
}

news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_params)
news_response.raise_for_status()
news_data = news_response.json()

stock_variation = int(stock_price_yesterday * 100 / stock_price_before) - 100
print(stock_variation)

if stock_price_yesterday >= (stock_price_before * 1.05) or stock_price_yesterday <= (stock_price_before * 0.95):
    print(sms_body(stock_variation, news_data, 1))
    for i in range(3):
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ.get('https_proxy')}
        client = Client(TWILLIO_ID, TWILLIO_TOKEN, http_client=proxy_client)
        message = client.messages \
            .create(
            body= f"{sms_body(stock_variation, news_data, i)}",
            from_='+12183767080',
            to='+541157095128'
)

