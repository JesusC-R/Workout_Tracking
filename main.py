import requests
import os
from datetime import datetime

MY_API_ID = os.environ['API_ID']
MY_API_KEY = os.environ["API_KEY"]

nutritionix_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'

params = {
    "query": input('What exercises did you do?\n'),
    "gender": "male",
    "weight_kg": 72.5,
    "height_cm": 167.64,
    "age": 30
}

headers = {
    'x-app-id': MY_API_ID,
    'x-app-key': MY_API_KEY,
}

nutrition_response = requests.post(url=nutritionix_endpoint, json=params, headers=headers)
# nutrition_response.raise_for_status()
result = nutrition_response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

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

    TOKEN = os.environ['BEARER']
    sheet_headers = {
        "Authorization": TOKEN
    }

    sheet_response = requests.post('https://api.sheety.co/9d7dfe2286aa4bc0831907c596b0202d/myWorkouts/workouts', headers=sheet_headers,
                                   json=sheet_inputs)

    print(sheet_response.text)
