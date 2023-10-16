from aiogram import Bot, Dispatcher
from bot.logs import logger
from bot.config_data.config import Config, load_config
from bot.handlers import main_handler


async def main():
    # Вывод информации о начале запуска бота
    logger.info("Bot is starting")

    # Загрузка конфига
    config: Config = load_config()

    # Инициализация бота + диспетчера
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистрация роутеров
    dp.include_router(main_handler.router)

    # Пропуск накопившихся апдейтов
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск поллинга (постоянного опроса сервера)
    await dp.start_polling(bot)
