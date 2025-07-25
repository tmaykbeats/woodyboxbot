import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  # Добавлены импорты
from .messages import send_main_menu
from telegram.ext import CallbackContext, CallbackQueryHandler
from src.config import config
from src.handlers.keyboards import (
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
        keyboard = [
            [InlineKeyboardButton("📅 Забронировать", url=config['booking_link'])],
            [InlineKeyboardButton("← Назад", callback_data='back')]
        ]
        
        await query.edit_message_text(
            text=f"🎹 Наши услуги:\n{services}\n\n{config['booking_text']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == 'products':  # Обработка товаров
        # Формируем список товаров с кнопками-ссылками
        products_list = []
        keyboard = []
        
        for product in config['products']:
            # Создаем кнопку с названием товара и ссылкой
            keyboard.append(
                [InlineKeyboardButton(product['name'], url=product['url'])]
            )
            # Формируем текст для списка
            products_list.append(f"• {product['name']}")
        
        # Добавляем кнопку "Назад"
        keyboard.append(
            [InlineKeyboardButton("⬅️ Назад", callback_data='back')]
        )
        
        await query.edit_message_text(
            text="🎵 Наши товары:\n\n" + "\n".join(products_list),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data == 'back':
        await send_main_menu(query.from_user.id, context)

def get_callbacks_handlers():
    """Возвращает обработчики кнопок"""
    return [
        CallbackQueryHandler(button_handler)
    ]