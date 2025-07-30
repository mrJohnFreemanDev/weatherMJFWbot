# 🌦️ weatherMJFWbot

A Telegram bot that provides current weather conditions for any city using the WeatherAPI service.

## 🌍 Features

- Get weather by city name in English or Russian
- Detects language automatically based on input
- Shows:
  - Temperature in °C and °F
  - Feels like temperature
  - Wind speed in km/h and mph
  - Wind direction with emoji
  - Country flags
  - Local time with time-of-day emoji
- Logs user queries to `clients.log`
- Error logging to `error.log`

## ⚙️ Tech Stack

- Python 3.10+
- Telebot (pyTelegramBotAPI)
- WeatherAPI
- requests
- dotenv
- pytz
- Logging and emoji-enhanced formatting

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weatherMJFWbot.git
cd weatherMJFWbot
```

### 2. Create `.env` file

```env
API_TOKEN=your_telegram_api_token
WAPI_KEY=your_weatherapi_key
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the bot

```bash
python weatherMJFWbot.py
```

## 📬 Contact

- Telegram: [@ivan_mudriakov](https://t.me/ivan_mudriakov)
- Email: [mr.john.freeman.works.rus@gmail.com](mailto:mr.john.freeman.works.rus@gmail.com)

---

☁️ Built with care by Ivan Mudriakov. Open to feedback and freelance projects.
