import logging

logger = logging.getLogger(__name__)

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d\n#%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)

# Обработчик для записи в файл
file_handler = logging.FileHandler("bot/logs/bot_logs.log")
logger.addHandler(file_handler)
