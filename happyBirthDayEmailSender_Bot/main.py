import pandas as pd
import smtplib
import datetime as dt
import random

APP_EMAIL = "bot706051@gmail.com"
APP_PASSWORD = "place_holder"

today_day = dt.datetime.now().day
today_month = dt.datetime.now().month

df = pd.read_csv("data.csv")
list_of_dicts = df.to_dict(orient='records')

for i in range(len(list_of_dicts)):
    if list_of_dicts[i]["Day"] == today_day and list_of_dicts[i]["Month"] == today_month:
        with open("allTextFilesNames") as file0:
            data = file0.read()
            txts = data.split("\n")
            txt = random.choice(txts)

        with open(txt, "r") as file:
            text = file.read()

        receiver_email = list_of_dicts[i]["Email"]
        receiver_name = list_of_dicts[i]["Name"]

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=APP_EMAIL, password=APP_PASSWORD)
            connection.sendmail(from_addr=APP_EMAIL,
                                to_addrs=receiver_email,
                                msg=f"Subject:Happy BD!\n\nHey {receiver_name}\n{text}")
    else:
        print("Nobody have birth day today!")

