import pytest
from unittest.mock import patch, AsyncMock
from handlers.callbacks import button_handler
import handlers.callbacks as callbacks_module  # Единый псевдоним для модуля
from telegram import InlineKeyboardButton

@pytest.mark.asyncio
async def test_prices_button(mock_update, mock_context):
    # Сохраняем оригинальный конфиг
    original_config = callbacks_module.config
    
    try:
        # Временная замена конфига
        callbacks_module.config = {
            'services': {"Тест": "1000₽"},
            'booking_text': "Бронирование",
            'info_content': {},
            'booking_link': "https://your-booking-link.com"  # Добавьте эту строку
        }
        
        # Устанавливаем данные callback
        mock_update.callback_query.data = 'prices'
        await button_handler(mock_update, mock_context)
        
        # Проверяем вызов edit_message_text
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        
        # Получаем аргументы вызова
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Тест: 1000₽" in kwargs['text']
        assert "Бронирование" in kwargs['text']
        
    finally:
        # Восстановление оригинального конфига
        callbacks_module.config = original_config

# Тест для кнопки "Полезная информация"
@pytest.mark.asyncio
async def test_info_button(mock_update, mock_context):
    # Сохраняем оригинальный конфиг
    original_config = callbacks_module.config
    
    try:
        # Временная замена конфига
        callbacks_module.config = {
            'info_content': {"Тест": "https://example.com"},
            'services': {},
            'booking_link': "https://booking.com",  # Добавить
            'booking_text': "Бронирование"          # Добавить
        }
        # Мокировать создание кнопок
        with patch('handlers.callbacks.InlineKeyboardMarkup') as mock_markup, \
            patch('handlers.callbacks.InlineKeyboardButton') as mock_button:
            
            mock_button.return_value = "mocked_button"
            mock_markup.return_value.inline_keyboard = [["mocked_button"]]
            
        # Устанавливаем данные callback
        mock_update.callback_query.data = 'info'
        await button_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Полезные материалы" in kwargs['text']
        assert "Тест: https://example.com" in kwargs['text']
        
    finally:
        # Восстановление оригинального конфига
        callbacks_module.config = original_config

# Тест для кнопки "Назад"
@pytest.mark.asyncio
async def test_back_button(mock_update, mock_context):
    mock_update.callback_query.data = 'back'
    await button_handler(mock_update, mock_context)
    
    mock_update.callback_query.edit_message_text.assert_awaited_once()
    args, kwargs = mock_update.callback_query.edit_message_text.call_args
    assert "Выберите действие:" in kwargs['text']