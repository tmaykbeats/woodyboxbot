import pytest
from unittest.mock import patch, AsyncMock
from handlers.callbacks import button_handler
from handlers import callbacks  # Импортируем модуль

@pytest.mark.asyncio
async def test_prices_button(mock_update, mock_context):
    # Временная замена конфига
    original_config = callbacks.config
    callbacks.config = {
        'services': {"Тест": "1000₽"},
        'booking_text': "Бронирование",
        'info_content': {}
    }
    
    # Устанавливаем данные callback
    mock_update.callback_query.data = 'prices'
    await button_handler(mock_update, mock_context)
    
    # Проверяем вызов edit_message_text у callback_query
    mock_update.callback_query.edit_message_text.assert_awaited_once()
    
    # Получаем аргументы вызова
    args, kwargs = mock_update.callback_query.edit_message_text.call_args
    assert "Тест: 1000₽" in kwargs['text']
    assert "Бронирование" in kwargs['text']
    
    # Восстановление оригинального конфига
    callbacks.config = original_config