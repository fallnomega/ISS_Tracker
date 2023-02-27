import requests
from datetime import datetime
import pytz
import smtplib

MY_LAT = 37.9319  # Your latitude
MY_LONG = -121.6958  # Your longitude


def get_hour(time):
    temp_hour = int(time.split("T")[1].split(":")[0])
    return temp_hour


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

# converting my time to UTC just to align with sunrise-sunset.org UTC time returned
time_now = datetime.now(tz=pytz.utc)
my_time = str(time_now)
my_hour = int(my_time.split(' ')[1].split(':')[0])
my_min = int(my_time.split(' ')[1].split(':')[1])

sunrise_hour = get_hour(data["results"]["sunrise"])
sunset_hour = get_hour(data["results"]["sunset"])

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look  up.

if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5) \
        and (my_hour >= sunset_hour or my_hour <= sunrise_hour):
    # print("True")
    email = "YOUR EMAIL"
    password = "YOUR PASSWORD"  # NOT SECURE BUT FOR LEARNING EXERCISE WE SHALL STORE IT HERE
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.ehlo()
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(from_addr=email,
                        to_addrs=email,
                        msg=f"Subject:ISS Incoming!\n\nLookup, ISS in the night time sky!")
    connection.close()
else:
    print("Not visible")
