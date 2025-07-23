import logging
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from .keyboards import main_menu_keyboard  # Относительный импорт
from .messages import send_main_menu  # Относительный импорт

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start - сразу показывает главное меню"""
    logger.debug(f"Получена команда /start от пользователя {update.effective_user.id}")
    user = update.effective_user
    
    try:
        # Всегда показываем главное меню
        await send_main_menu(user.id, context)
        logger.info(f"Главное меню отправлено пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")

def get_commands_handlers():
    """Возвращает обработчики команд"""
    return [
        CommandHandler("start", start)
    ]