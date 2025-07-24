import pytest
from handlers.callbacks import button_handler

@pytest.mark.asyncio
async def test_prices_button(mock_update, mock_context, monkeypatch):
    # Подменяем конфиг
    monkeypatch.setattr('handlers.callbacks.config', {
        'services': {"Тест": "1000₽"},
        'booking_text': "Бронирование",
        'info_content': {}
    })
    
    # Эмулируем нажатие кнопки "prices"
    mock_update.callback_query.data = 'prices'
    
    await button_handler(mock_update, mock_context)
    
    # Проверяем изменение текста сообщения
    mock_context.bot.edit_message_text.assert_called_once()
    args, kwargs = mock_context.bot.edit_message_text.call_args
    assert "Тест: 1000₽" in kwargs['text']
    assert "Бронирование" in kwargs['text']