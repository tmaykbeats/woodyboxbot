import logging
from telegram.ext import Application
from config import BOT_TOKEN
from handlers.commands import get_commands_handlers
from handlers.callbacks import get_callbacks_handlers
from handlers.events import get_events_handlers
import sys
sys.path.append('utils')  # Добавляем путь к папке utils

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Запуск бота"""
    try:
        logger.info("Запуск бота...")
        application = Application.builder().token(BOT_TOKEN).build()

        # Регистрация обработчиков
        for handler in get_commands_handlers():
            application.add_handler(handler)
            
        for handler in get_callbacks_handlers():
            application.add_handler(handler)
            
        for handler in get_events_handlers():
            application.add_handler(handler)

        # Запуск бота
        logger.info("Бот успешно инициализирован")
        application.run_polling()
        logger.info("Бот запущен и работает...")
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()