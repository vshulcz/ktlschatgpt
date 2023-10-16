from dataclasses import dataclass
from environs import Env


@dataclass
class tgbot:
    token: str  # Токен бота


@dataclass
class Config:
    tg_bot: tgbot


# Функция, которая будет читать .env и возвращать объект класса Config с заполненным
# полем token
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=tgbot(token=env("BOT_TOKEN")))


# Функция, которая будет читать .env и возвращать вайтлист
def load_whitelist(path: str | None = None) -> list:
    env = Env()
    env.read_env(path)
    return env("WHITELIST").split(",")
