from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import config

def main_menu_keyboard():
    """Клавиатура главного меню"""
    keyboard = [
        [InlineKeyboardButton("💰 Прайс-лист", callback_data='prices')],
        [InlineKeyboardButton("ℹ️ Полезная информация", callback_data='info')],
        [InlineKeyboardButton("📞 Связаться с нами", url=config['booking_link'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_menu_keyboard():
    """Клавиатура для возврата в главное меню"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("← Назад", callback_data='back')]
    ])

def booking_keyboard():
    """Клавиатура для бронирования"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Забронировать", url=config['booking_link'])]
    ])