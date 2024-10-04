import requests
import smtplib
import pandas as pd
import random


APP_EMAIL = "bot706051@gmail.com"
APP_PASSWORD = "place_holder"

file = pd.read_csv("emailData.csv")
data = file.to_dict(orient="index")

api_key = requests.get(url="http://api.open-notify.org/iss-now.json")
api_data = api_key.json()

latitude = float(api_data["iss_position"]["latitude"])
longitude = float(api_data["iss_position"]["longitude"])

print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

if (40 < latitude < 45) and (20 < longitude < 27):
    with open("texts.txt", "r") as file:
        list_of_texts = file.readlines()

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=APP_EMAIL, password=APP_PASSWORD)
        for i in range(0, len(data)):
            txt = random.choice(list_of_texts)
            connection.sendmail(from_addr=APP_EMAIL,
                                to_addrs=data[i]["Email"],
                                msg=f"Subject:Hi {data[i]['Name']}!\n\n{txt}")
    print("Emails have been sent!")
else:
    print("ISS is not around!")
