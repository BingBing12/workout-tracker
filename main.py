import requests
import datetime
from decouple import config

APP_ID = config("APP_ID")
APP_KEY = config("APP_KEY")
SHEET_TOKEN = config("TOKEN")
SHEET_URL = "https://api.sheety.co/3e87c31021d0bd3e249cbfcba52d2d15/myWorkouts/workouts"
workout_params = {
    "query": input("What did you train today"),
}
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

nutrionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=nutrionix_endpoint, json=workout_params, headers=headers)
result = response.json()

today_date = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")

header = {
    "Authorization": SHEET_TOKEN
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(SHEET_URL, json=sheet_inputs, headers=header)

print(sheet_response.text)
