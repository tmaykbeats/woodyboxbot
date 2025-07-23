import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from keyboards import main_menu_keyboard
from utils.messages import send_main_menu

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

async def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start"""
    logger.debug(f"Получена команда /start от пользователя {update.effective_user.id}")
    user = update.effective_user
    
    try:
        # Всегда отправляем главное меню
        await send_main_menu(user.id, context)
        logger.info(f"Главное меню отправлено пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")

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