import logging
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from src.config import config
from src.handlers.keyboards import (  # Изменено
    main_menu_keyboard,
    back_to_menu_keyboard,
    booking_keyboard
)

logger = logging.getLogger(__name__)

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == 'prices':
        services = "\n".join([f"- {s}: {p}" for s, p in config['services'].items()])
        await query.edit_message_text(
            text=f"🎹 Наши услуги:\n{services}\n\n{config['booking_text']}",
            reply_markup=booking_keyboard()
        )

def get_callbacks_handlers():
    """Возвращает обработчики кнопок"""
    return [
        CallbackQueryHandler(button_handler)
    ]