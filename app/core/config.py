import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Autonomous Data Analyst"
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development"
    )

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )


settings = Settings()