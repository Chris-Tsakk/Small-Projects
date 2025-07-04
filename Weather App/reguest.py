import requests
import json


def get_full_weather(city):
    url = f'https://wttr.in/{city}?format=j1'  # Παίρνει όλα τα δεδομένα σε JSON
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Μετατροπή της απόκρισης σε Python dictionary

        weather_data = {
            "city": city,
            "condition": data["current_condition"][0]["weatherDesc"][0]["value"],  # Καιρός
            "temperature": data["current_condition"][0]["temp_C"] + "°C",  # Θερμοκρασία
            "wind": data["current_condition"][0]["windspeedKmph"] + " km/h",  # Άνεμος
            "humidity": data["current_condition"][0]["humidity"] + "%",  # Υγρασία
            "feels_like": data["current_condition"][0]["FeelsLikeC"] + "°C",  # Αίσθηση θερμοκρασίας
            "pressure": data["current_condition"][0]["pressure"] + " hPa",  # Ατμοσφαιρική πίεση
            "uv_index": data["current_condition"][0]["uvIndex"]  # Δείκτης UV
        }

        # Αποθήκευση σε JSON αρχείο
        with open("weather_data.json", "w") as file:
            json.dump(weather_data, file, indent=4)

        print("Weather data saved.")
    else:
        print("Failed to retrieve weather data.")


