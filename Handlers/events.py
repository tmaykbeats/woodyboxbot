import logging
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from .messages import send_main_menu
from config import CHANNEL_ID

logger = logging.getLogger(__name__)

async def handle_new_members(update: Update, context: CallbackContext) -> None:
    """Обработка новых участников канала - отправляем главное меню"""
    try:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
                
            # Отправляем сразу главное меню
            await send_main_menu(member.id, context)
            logger.info(f"Главное меню отправлено новому участнику {member.id}")
                
    except Exception as e:
        logger.error(f"Ошибка обработки новых участников: {e}")

def get_events_handlers():
    """Возвращает обработчики событий"""
    return [
        MessageHandler(
            filters.Chat(chat_id=CHANNEL_ID) & filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_new_members
        )
    ]