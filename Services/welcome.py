import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import config
from services.notifications import notify_user_in_channel
from utils.messages import send_main_menu

logger = logging.getLogger(__name__)

async def send_welcome_message(user_id: int, context: CallbackContext):
    """Отправка приветственного сообщения с кнопкой Start"""
    try:
        logger.info(f"Попытка отправить приветствие пользователю {user_id}")
        
        # Создаем кнопку Start
        start_button = InlineKeyboardButton(
            "🚀 Start", 
            url=f"https://t.me/{context.bot.username}?start=init"
        )
        keyboard = InlineKeyboardMarkup([[start_button]])
        
        await context.bot.send_message(
            chat_id=user_id,
            text=config['welcome_message'],
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        logger.info(f"Приветствие отправлено пользователю {user_id}")
        return True
    except telegram.error.Forbidden as e:
        error_message = str(e).lower()
        if "bot was blocked by the user" in error_message:
            logger.warning(f"Пользователь {user_id} заблокировал бота")
        elif any(msg in error_message for msg in ["user not found", "user has not started conversation"]):
            logger.info(f"У пользователя {user_id} закрыты ЛС для ботов")
            await notify_user_in_channel(user_id, context)
        return False
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")
        return False