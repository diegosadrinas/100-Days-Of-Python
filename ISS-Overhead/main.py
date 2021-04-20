import requests
from datetime import datetime
import smtplib
import time
from dotenv import dotend_values


MY_LAT = -34.603683
MY_LONG = -58.381557
MY_EMAIL = config["MY_EMAIL"]
MY_PASS = config["MY PASS"]
TO_EMAIL = config["TO_EMAIL"]



def iss_above():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_above() and is_night():
        MY_EMAIL = "sadrinastest@gmail.com"
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL,
                            msg="Subject: ISS getting close!\n\nLook up in the sky. ISS is flying above.")
        connection.close()

