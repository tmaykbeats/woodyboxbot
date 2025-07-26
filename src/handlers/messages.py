import logging
from telegram.ext import CallbackContext
from src.handlers.keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)

async def send_main_menu(user_id: int, context: CallbackContext):
    """Отправка главного меню"""
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="Добро пожаловать! Выберите действие:",
            reply_markup=main_menu_keyboard()
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке главного меню: {e}")
        return False