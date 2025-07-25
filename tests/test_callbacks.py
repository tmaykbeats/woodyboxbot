import pytest
from unittest.mock import patch, AsyncMock
from handlers.callbacks import button_handler
import handlers.callbacks as callbacks_module  # Единый псевдоним для модуля

@pytest.mark.asyncio
async def test_prices_button(mock_update, mock_context):
    # Сохраняем оригинальный конфиг
    original_config = callbacks_module.config
    
    try:
        # Временная замена конфига
        callbacks_module.config = {
            'services': {"Тест": "1000₽"},
            'booking_text': "Бронирование",
            'info_content': {}
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
            'services': {}
        }
        
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