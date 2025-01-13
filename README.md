# Python Telegram Bot on Aiogram with Docker Compose

This repository contains a Python Telegram bot built using the [Aiogram](https://docs.aiogram.dev/) framework. The bot is designed to be easily deployed and run using Docker Compose.

- ## Technologies Used

The following technologies and libraries are used in this project:

- **Aiogram**: For building the Telegram bot.
- **SQLAlchemy**: For database interactions.
- **Pydantic**: For data validation and settings management.
- **Alembic**: For database migrations.
- **Open-Meteo API**: For fetching weather data.
- **APScheduler**: For scheduling periodic weather reports.
- **Docker Compose**: For seamless deployment.

## Requirements

- Docker Compose
- Telegram Bot Token

## Setup and Deployment

Follow these steps to deploy the bot:

### 1. Clone the Repository

```bash
git clone https://github.com/IRIT-RTF-projects/python-telegram-bot.git
cd your-repo-name
```

### 2. Create and Configure the .env File

Create a .env file in the root directory of the project and set the following variables:

```
TOKEN=<your_telegram_bot_token>
DB__URL = postgresql+asyncpg://postgres:postgres@localhost:5432/bot_db
```
Replace <your_telegram_bot_token> with your actual Telegram bot token obtained from BotFather.

Also it is recomended but not required to replace postgres user password in docker-compose.yaml and in the connection string

### 3. Build and Run the Docker Containers

Use Docker Compose to build and run the containers:

```bash
docker-compose up --build -d
```

### 4. Verify the Bot is Running

Check the logs to ensure the bot is running without errors:

```bash
docker-compose logs -f
```

Your bot should now be up and running!


```
├── main.py               # Main entry point of the bot
├── config.py             # Configuration loader
├── alembic               # Alembic migration directory, modify carefully
├── crud
│   └── crud_base.py      # Implementaion of base crud operation using sqlalchemy orm
├── handlers
│   ├── utils.py          # crud calls for handlers
│   ├── text_commands.py  # Definitions of commands or callbacks given by text
│   ├── help.py           # Shows the help text
│   ├── locations.py      # Location management
│   ├── subscriptions.py  # Subscription management
│   ├── weather_by_geo.py # Shows weather when geo is sent
│   └── main_menu.py      # Shows main menu inline
├── models
│   ├── db.py             # Engine and sessionmaker initialization
│   └── models.py         # Definition of db models
├── presets               # All the preset messages
├── subscription_manager
│   └── send_reports.py   # Subscription reports handler
├── weather_requests
│   └── weather.py        # Class that makes the api call and formats the answer to text
├── docker-compose.yml    # Docker Compose configuration file
├── Dockerfile            # Dockerfile for the bot
├── .env                  # Environment variables file
└── README.md             # Project documentation
```

## Extending the Bot

1. Add new handlers in the python-telegram-bot/handlers directory.
2. Register the handlers in python-telegram-bot/main.py.
3. Rebuild the Docker image if necessary:
```bash
docker compose down
docker compose up --build -d
```

## Troubleshooting

1. If you encounter issues, ensure your .env file is correctly configured.
2. Check the logs for detailed error messages:
```bash
docker-compose logs -f --tail <number_of_lines_from_end>
```
3. Ensure you have the latest version of Docker and Docker Compose installed.

#### Happy bot building! 🚀
