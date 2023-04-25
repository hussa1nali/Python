# import random module
import random

# create a list of tuples containing weather data for each day
weather_data = [
    ("2023-04-17", 15, 10, 20, "cloudy"),
    ("2023-04-18", 18, 12, 22, "sunny"),
    ("2023-04-19", 16, 11, 21, "cloudy"),
    ("2023-04-20", 19, 14, 24, "sunny"),
    ("2023-04-21", 20, 15, 25, "sunny"),
    ("2023-04-22", 17, 12, 21, "rainy"),
    ("2023-04-23", 13, 8, 18, "rainy"),
    ("2023-04-24", 16, 10, 22, "cloudy")
]

# get today's weather data
today_date = "2023-04-24"
today_weather = [data for data in weather_data if data[0] == today_date][0]

# get last week's weather data for the same day
last_week_date = "2023-04-17"
last_week_weather = [data for data in weather_data if data[0] == last_week_date][0]

# compare the temperature and weather condition for today and last week's same day
if today_weather[1] > last_week_weather[1]:
    temp_change = "warmer"
elif today_weather[1] < last_week_weather[1]:
    temp_change = "cooler"
else:
    temp_change = "about the same"

if today_weather[4] != last_week_weather[4]:
    weather_change = "different"
else:
    weather_change = "about the same"

# print the weather comparison results
print(f"Today's temperature ({today_weather[1]}°C) is {temp_change} than last week's temperature ({last_week_weather[1]}°C).")
print(f"The weather condition today ({today_weather[4]}) is {weather_change} than last week's weather condition ({last_week_weather[4]}).")
