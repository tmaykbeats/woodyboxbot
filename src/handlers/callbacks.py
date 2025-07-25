import logging
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from .keyboards import main_menu_keyboard, back_to_menu_keyboard, booking_keyboard
from ..config import config

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
    
    elif query.data == 'info':
        info = "\n".join([f"• {k}: {v}" for k, v in config['info_content'].items()])
        await query.edit_message_text(
            text=f"📚 Полезные материалы:\n\n{info}",
            reply_markup=back_to_menu_keyboard()
        )
    
    elif query.data == 'back':
        await query.edit_message_text(
            text="Выберите действие:",
            reply_markup=main_menu_keyboard()
        )

def get_callbacks_handlers():
    """Возвращает обработчики кнопок"""
    return [
        CallbackQueryHandler(button_handler)
    ]