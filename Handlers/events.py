import logging
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from services.welcome import send_welcome_message
from config import CHANNEL_ID

logger = logging.getLogger(__name__)

async def handle_new_members(update: Update, context: CallbackContext) -> None:
    """Обработка новых участников канала"""
    try:
        for member in update.message.new_chat_members:
            # Игнорируем самого бота
            if member.id == context.bot.id:
                continue
                
            # Пытаемся отправить приветственное сообщение
            if not await send_welcome_message(member.id, context):
                logger.info(f"Не удалось отправить ЛС пользователю {member.id}")
                
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