import logging
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from services.welcome import send_welcome_message
from config import CHANNEL_ID

logger = logging.getLogger(__name__)

async def handle_new_members(update: Update, context: CallbackContext) -> None:
    """Обработка новых участников канала"""
    try:
        logger.info(f"Получено обновление: {update}")
        logger.info(f"Новые участники: {update.message.new_chat_members}")
        
        # Для каждого нового участника
        for member in update.message.new_chat_members:
            logger.info(f"Новый участник: {member.id} ({member.username})")
            
            # Игнорируем, если это сам бот
            if member.id == context.bot.id:
                logger.info("Бот добавлен в канал")
                await update.message.reply_text("Бот активирован! Ожидаю новых участников.")
                continue
                
            # Пытаемся отправить приветственное сообщение
            await send_welcome_message(member.id, context)
            
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