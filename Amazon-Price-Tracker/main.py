from bs4 import BeautifulSoup
import lxml
import requests
import smtplib
from decouple import config

MY_EMAIL = config("MY_EMAIL")
PASSWORD = config("PASSWORD")
TO_EMAIL = config("TO_EMAIL")

# request info
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "es-xl",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

response = requests.get("https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B06Y1MP2PY/ref=sr_1_1?qid=1597662463&th=1",
                        headers=headers)
amazon_product_webpage = response.text

# scrap with bs
soup = BeautifulSoup(amazon_product_webpage, "lxml")
product_price = soup.find(id="priceblock_ourprice").getText().split()[1]

# send email
initial_product_price = 139.99
message = f"Subject: Amazon Price Tracker\n\nThe product you're interested on has dropped its price to {product_price} "
if float(product_price) < initial_product_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=message)
        print("email sent")
        connection.close()

