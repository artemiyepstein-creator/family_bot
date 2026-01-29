from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str

def get_settings() -> Settings:
    bot_token = getenv("BOT_TOKEN")
    database_url = getenv("DATABASE_URL")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set in .env")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in .env")
    
    return Settings(
        bot_token=bot_token,
        database_url=database_url,
    )