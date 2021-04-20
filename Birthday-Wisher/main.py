
import pandas as pd
import datetime as dt
import smtplib
from dotenv import dotenv_values

config = dotenv_valuea(".env")
file = pd.read_csv("birthdays.csv")
df = pd.DataFrame(file)
file_dict = df.to_dict("records")

now = dt.datetime.now()
today = (now.month, now.day)

for i in file_dict:
    if (i["month"], i["day"]) == today:
        with open("./letter_templates/letter_1.txt") as letter:
            content = letter.read()
            content = content.replace("[NAME]", i['name'])
            myemail = config["myemail"]
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=myemail, password=config["mypassword"])
            connection.sendmail(from_addr=myemail, to_addrs="sample@adress.com ", msg=f"Subject: Happy Birthday!\n\n"
                                                                                        f"{content}\n")
            connection.close()







