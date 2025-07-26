import logging
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from .messages import send_main_menu
from src.config import config
from src.handlers.commands import send_main_menu

logger = logging.getLogger(__name__)

async def handle_new_members(update: Update, context: CallbackContext) -> None:
    """Обработка новых участников канала - отправляем главное меню"""
    try:
        # Логируем полученное событие
        logger.debug(f"Получено событие новых участников в чате {update.message.chat.id}")
        
        # Проверяем, что событие произошло в нужном канале
        if update.message.chat.id != config['CHANNEL_ID']:
            logger.warning(f"Событие не в целевом канале! Получено: {update.message.chat.id}, ожидалось: {config['CHANNEL_ID']}")
            return
            
        logger.info(f"Событие в целевом канале ({config['CHANNEL_ID']})")
        
        # Получаем ID бота
        bot_id = context.bot.id
        logger.debug(f"ID бота: {bot_id}")
            
        # Исправлено: используем update.message.new_chat_members вместо new_chat_members
        for member in update.message.new_chat_members:
            # Логируем информацию о новом участнике
            logger.info(f"Новый участник: ID={member.id}, Имя={member.first_name}, Бот={member.is_bot}")
            
            # Пропускаем самого бота
            if member.is_bot:
                logger.info("Пропускаем бота")
                continue
                
            # Отправляем главное меню
            logger.info(f"Отправляем главное меню пользователю {member.id}")
            try:
                await send_main_menu(member.id, context)
                logger.info(f"Главное меню отправлено новому участнику {member.id}")
            except Exception as e:
                logger.error(f"Ошибка при отправке меню: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка обработки новых участников: {e}", exc_info=True)

# Добавляем экспорт функции
def get_events_handlers():
    """Возвращает обработчики событий"""
    return [
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_new_members
        )
    ]