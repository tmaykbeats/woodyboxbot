import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import CHANNEL_ID, config

logger = logging.getLogger(__name__)

async def notify_user_in_channel(user_id: int, context: CallbackContext):
    """Уведомление пользователя в канале о попытке связи"""
    try:
        logger.info(f"Отправка уведомления в канал для пользователя {user_id}")
        
        # Пытаемся получить информацию о пользователе
        try:
            user_chat = await context.bot.get_chat(user_id)
            user_name = user_chat.username or user_chat.full_name
        except:
            user_name = f"пользователь с ID {user_id}"
        
        # Формируем текст сообщения
        text = (
            f"Привет, {user_name}! 🎤\n"
            "Мы пытались отправить вам приветственное сообщение, но не смогли.\n\n"
            "Чтобы получить важную информацию, нажмите кнопку ниже:"
        )
        
        keyboard = [
            [InlineKeyboardButton(
                "🚀 Start", 
                url=f"https://t.me/{context.bot.username}?start=init"
            )]
        ]
        
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
        logger.info(f"Уведомление для пользователя {user_id} отправлено в канал")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в канал: {e}")