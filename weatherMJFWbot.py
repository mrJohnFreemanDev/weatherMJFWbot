import json
import telebot
import requests
import logging
from datetime import datetime
import pytz
import re

load_dotenv("all.env")
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)

def log_client_request(user_id, username, query):
    gmt_time = datetime.now(pytz.timezone('GMT')).strftime('%Y-%m-%d %H:%M:%S')
    with open("clients.log", "a") as clients_log:
        clients_log.write(f"Time: {gmt_time}\nUser ID: {user_id}\nUsername: {username}\nQuery: {query}\n")

def get_wind_direction(dir_code, lang='en'):
    directions_en = {
        "N": "North 🌍",
        "NE": "Northeast 🌍",
        "E": "East 🌍",
        "SE": "Southeast 🌍",
        "S": "South 🌍",
        "SW": "Southwest 🌍",
        "W": "West 🌍",
        "NW": "Northwest 🌍"
    }
    directions_ru = {
        "N": "Север 🌍",
        "NE": "Северо-восток 🌍",
        "E": "Восток 🌍",
        "SE": "Юго-восток 🌍",
        "S": "Юг 🌍",
        "SW": "Юго-запад 🌍",
        "W": "Запад 🌍",
        "NW": "Северо-запад 🌍"
    }
    if lang == 'ru':
        return directions_ru.get(dir_code, dir_code)
    return directions_en.get(dir_code, dir_code)

def get_weather_emoji(temp_c):
    if temp_c <= 0:
        return "❄️"  # Snowflake
    elif temp_c <= 15:
        return "🌧️"  # Cloud with rain
    elif temp_c <= 25:
        return "🌤️"  # Sun with small cloud
    else:
        return "☀️"  # Sun

def get_time_of_day_emoji(local_time):
    hour = int(local_time.split(' ')[1].split(':')[0])
    if 6 <= hour < 18:
        return "🌅"  # Sunrise
    else:
        return "🌃"  # Night with stars

def get_country_flag_emoji(country_code):
    if len(country_code) == 2 and country_code.isalpha():
        return chr(127462 + ord(country_code.upper()[0]) - ord('A')) + chr(127462 + ord(country_code.upper()[1]) - ord('A'))
    return "🏳️"

def convert_kph_to_mph(kph):
    return round(kph * 0.621371, 1)

def convert_c_to_f(celsius):
    return round(celsius * 9/5 + 32, 1)

@bot.message_handler(content_types=['text'])
def asking(message):
    try:
        log_client_request(message.from_user.id, message.from_user.username, message.text)
        lang = 'ru' if re.search('[\u0400-\u04FF]', message.text) else 'en'
        response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={WAPI_KEY}&q={message.text}&aqi=no'
        )
        response.raise_for_status()
        data = response.json()
        loc = data["location"]
        cur = data["current"]
        name = loc['name']
        country = loc['country']
        country_code = loc.get('country_code', 'unknown')
        local_time = loc['localtime']
        temp_c = cur['temp_c']
        temp_f = convert_c_to_f(temp_c)
        feels_like_c = cur['feelslike_c']
        feels_like_f = convert_c_to_f(feels_like_c)
        wind_speed_kph = cur['wind_kph']
        wind_speed_mph = convert_kph_to_mph(wind_speed_kph)
        wind_dir = get_wind_direction(cur['wind_dir'], lang)
        weather_emoji = get_weather_emoji(temp_c)
        time_of_day_emoji = get_time_of_day_emoji(local_time)
        country_flag_emoji = get_country_flag_emoji(country_code)

        if lang == 'ru':
            result = (
                f"{time_of_day_emoji} Местное время: {local_time}\n"
                f"{name}, {country_flag_emoji} {country}\n"
                f"Температура: {temp_c}°C (F: {temp_f}°F) {weather_emoji} (Ощущается как: {feels_like_c}°C ({feels_like_f}°F))\n"
                f"🌬️ Ветер: {wind_speed_kph} км/ч ({wind_speed_mph} м/ч), Направление: {wind_dir}"
            )
        else:
            result = (
                f"{time_of_day_emoji} Local time: {local_time}\n"
                f"{name}, {country_flag_emoji} {country}\n"
                f"Temperature: {temp_c}°C ({temp_f}°F) {weather_emoji} (Feels like: {feels_like_c}°C ({feels_like_f}°F))\n"
                f"🌬️ Wind: {wind_speed_kph} km/h ({wind_speed_mph} mph), Direction: {wind_dir}"
            )

    except requests.exceptions.RequestException as e:
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
        logging.error(f"{moscow_time} - User: {message.from_user.id} ({message.from_user.username}), Error code: {response.status_code}, Error: {e}")
        if lang == 'ru':
            result = "Извините, не нахожу данной локации."
        else:
            result = "Sorry, I cannot find this location."
    except KeyError as e:
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
        logging.error(f"{moscow_time} - User: {message.from_user.id} ({message.from_user.username}), Missing key: {e}")
        if lang == 'ru':
            result = "Извините, не нахожу данной локации."
        else:
            result = "Sorry, I cannot find this location."

    bot.reply_to(message, result)

bot.infinity_polling()
