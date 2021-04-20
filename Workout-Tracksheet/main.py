import requests
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")

APP_ID = config["APP_ID"]
APP_KEY = "APP_KEY"
SHEETY_USER = config["SHEETY_USER"]
SHEETY_PASS = config["SHETTY_PASS"]


# nutritionix
nutri_endpoint = "https://trackapi.nutritionix.com"
nutri_post_endpoint = f"/v2/natural/exercise/"

nutri_headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0"

}

nutri_params = {
    "query": input("What was your exercise today? "),
    "gender": "male",
    "weight_kg": 71,
    "height_cm": 187,
    "age": 36
}

app_response = requests.post(url=f"{nutri_endpoint}{nutri_post_endpoint}", json=nutri_params, headers=nutri_headers)
print(app_response.text)
exercise_data = app_response.json()
exercises = exercise_data["exercises"]

# Sheety
sheety_endpoint = "https://api.sheety.co/929474b28794ea4224e4e966b4706d83/myWorkouts/workouts"
sheety_header = {
    "Authorization": "Basic ZHNhZHJpbmFzOndvcmtvdXRzcGFzcw=="
}

sheety_response = requests.get(url=sheety_endpoint, headers=sheety_header)
data = sheety_response.json()
today = datetime.now()

for exercise in exercises:
    workout_content = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    add_row = requests.post(url=sheety_endpoint, json=workout_content, auth=(SHEETY_USER, SHEETY_PASS))
print(data)

