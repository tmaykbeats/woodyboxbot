import logging
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start"""
    logger.debug(f"Получена команда /start от пользователя {update.effective_user.id}")
    
    user = update.effective_user
    try:
        await update.message.reply_text(
            "Привет! Я помощник студии WoodyBox Rec.\nВыберите действие:",
            reply_markup=main_menu_keyboard()
        )
        logger.info(f"Ответ на /start отправлен пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")

async def test(update: Update, context: CallbackContext):
    """Тестовая команда для проверки отправки сообщений"""
    from services.welcome import send_welcome_message
    user_id = update.effective_user.id
    await send_welcome_message(user_id, context)

def get_commands_handlers():
    """Возвращает обработчики команд"""
    return [
        CommandHandler("start", start),
        CommandHandler("test", test)
    ]