import g4f

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bot.logs import logger
from bot.lexicon.lexicon import LEXICON
from bot.config_data.config import load_whitelist
from bot.database.database import users_chat_history, users_chat_history_template

# Инициализация роутера
router: Router = Router()

# Инициализация вайтлиста и истории для него
whitelist: list = load_whitelist()


async def gpt_request(message: Message) -> str:
    """Функция для отправки сообщений ChatGPT"""

    text = message.text
    answer = ""

    try:
        users_chat_history[message.from_user.id].append(
            {"role": "user", "content": text}
        )

        response = await g4f.ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=users_chat_history[message.from_user.id],
        )

        for msg in response:
            answer += msg

        users_chat_history[message.from_user.id].append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        logger.warning(e)
        answer = "Кажется, что-то пошло не так. Попробуйте позже."

    return answer


# Хэндлер на команду "/start" - добавлять пользователя в базу данных,
# если его там еще не было и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_chat_history:
        users_chat_history[message.from_user.id] = users_chat_history_template


# Хэндлер на команду "/help" - предоставить справочную информации
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Хэндлер на команду "/newchat" - очистить историю чата
@router.message(Command(commands="newchat"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])
    users_chat_history[message.from_user.id] = users_chat_history_template


# Хэндлер будет выдавать ответ от ChatGPT
@router.message(F.text)
async def send_answer(message: Message):
    if str(message.from_user.id) in whitelist:
        if message.from_user.id not in users_chat_history:
            users_chat_history[message.from_user.id] = users_chat_history_template
        await message.answer(await gpt_request(message))
    else:
        await message.answer(
            "Кажется, вам нельзя пользоваться этим ботом, обратитесь к администратору @vtrinitty"
        )
