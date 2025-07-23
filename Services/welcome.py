import logging
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from config import config, CHANNEL_ID
from services import notifications
from keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)

async def send_welcome_message(user_id: int, context: CallbackContext):
    """Отправка приветственного сообщения с обработкой ошибок"""
    try:
        logger.info(f"Попытка отправить приветствие пользователю {user_id}")
        await context.bot.send_message(
            chat_id=user_id,
            text=config['welcome_message'],
            reply_markup=main_menu_keyboard()
        )
        logger.info(f"Приветствие отправлено пользователю {user_id}")
        return True
    except telegram.error.Forbidden as e:
        error_message = str(e).lower()
        if "bot was blocked by the user" in error_message:
            logger.warning(f"Пользователь {user_id} заблокировал бота")
        elif "user not found" in error_message or "user has not started conversation with the bot" in error_message:
            logger.info(f"У пользователя {user_id} закрыты ЛС для ботов")
            await notifications.notify_user_in_channel(user_id, context)
        return False
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")
        return False