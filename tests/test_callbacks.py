import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from handlers.callbacks import button_handler
import handlers.callbacks as callbacks_module  # Единый псевдоним для модуля
from telegram import InlineKeyboardButton

@pytest.mark.asyncio
async def test_back_button(mock_update, mock_context):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'welcome_message': "Test Welcome",
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
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
async def test_info_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'info_content': {"Тест": "https://example.com"},
            'services': {"Услуга": "500₽"},  # Добавляем для полноты конфига
            'booking_link': "https://booking.com",
            'booking_text': "Бронирование"
        }
        
        # Упрощаем мокирование клавиатуры
        with patch('handlers.callbacks.InlineKeyboardMarkup') as mock_markup:
            mock_markup.return_value = MagicMock(inline_keyboard=[])
            
        mock_update.callback_query.data = 'info'
        await button_handler(mock_update, mock_context)
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        
    finally:
        callbacks_module.config = original_config

# Тест для кнопки "Назад"
@pytest.mark.asyncio
async def test_back_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'welcome_message': "Test Welcome",
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'back'
        
        # Устанавливаем ID пользователя для callback_query.from_user
        mock_update.callback_query.from_user.id = 123
        
        # Патчим send_main_menu
        with patch('handlers.callbacks.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
            await button_handler(mock_update, mock_context)
            
            # Проверяем вызов send_main_menu с правильными аргументами
            mock_send_menu.assert_awaited_once_with(123, mock_context)
            
    finally:
        callbacks_module.config = original_config

@pytest.mark.asyncio
async def test_prices_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'services': {"Test Service": "1000₽"},
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'prices'
        await button_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Test Service: 1000₽" in kwargs['text']
        
    finally:
        callbacks_module.config = original_config