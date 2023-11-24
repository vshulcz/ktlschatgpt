from gpt4free.g4f import ChatCompletion

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bot.logs import logger
from bot.lexicon.lexicon import LEXICON
from bot.config_data.config import load_whitelist
from bot.database.database import ChatUser, ChatMessage, ChatDatabase

# Инициализация роутера
router: Router = Router()

# Инициализация вайтлиста
whitelist: list = load_whitelist()

# Инициализация базы данных
db = ChatDatabase("chat_history.db")


async def gpt_request(message: Message) -> str:
    """Функция для отправки сообщений ChatGPT"""

    text = message.text
    answer = ""

    try:
        user = db.get_or_create_user(message.from_user.id)
        db.add_message(user, "user", text)

        response = await ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=db.get_user_history(user),
        )

        for msg in response:
            answer += msg

        db.add_message(user, "assistant", answer)

    except Exception as e:
        logger.warning(e)
        answer = "Кажется, что-то пошло не так. Попробуйте позже."

    return answer


# Хэндлер на команду "/start" - добавлять пользователя в базу данных,
# если его там еще не было и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    user = db.get_or_create_user(message.from_user.id)
    db.set_user_history(user)


# Хэндлер на команду "/help" - предоставить справочную информации
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Хэндлер на команду "/newchat" - очистить историю чата
@router.message(Command(commands="newchat"))
async def process_newchat_command(message: Message):
    await message.answer(LEXICON[message.text])
    user = db.get_or_create_user(message.from_user.id)
    db.set_user_history(user)


# Хэндлер будет выдавать ответ от ChatGPT
@router.message(F.text)
async def send_answer(message: Message):
    if str(message.from_user.id) in whitelist:
        db.get_or_create_user(message.from_user.id)
        await message.answer(await gpt_request(message))
    else:
        await message.answer(
            "Кажется, вам нельзя пользоваться этим ботом, обратитесь к администратору @vtrinitty"
        )
