import logging
from telegram.ext import CallbackContext
from config import CHANNEL_ID

logger = logging.getLogger(__name__)

async def notify_user_in_channel(user_id: int, context: CallbackContext):
    """Уведомление пользователя в канале о попытке связи"""
    try:
        logger.info(f"Отправка уведомления в канал для пользователя {user_id}")
        
        # Формируем текст сообщения
        text = (
            "Привет! Основатель WoodyBoxRec пытался отправить вам важное сообщение.\n\n"
            "Пожалуйста, выполните следующие шаги:\n"
            "1. Перейдите в [Настройки конфиденциальности](https://t.me/settings/privacy)\n"
            "2. В разделе 'Группы и каналы' выберите 'Кто может приглашать меня в группы и каналы?'\n"
            "3. Установите 'Все'\n\n"
            "После этого нажмите кнопку ниже, чтобы получить сообщение:"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔓 Получить приветственное сообщение", 
                                 url=f"https://t.me/{context.bot.username}?start=welcome")]
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