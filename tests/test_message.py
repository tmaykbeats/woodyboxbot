import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.handlers.messages import send_main_menu

@pytest.mark.asyncio
async def test_send_main_menu(mock_context):
    # Создаем мок клавиатуры
    mock_keyboard = MagicMock()
    
    # Исправляем путь для патча (правильный модуль)
    with patch('src.handlers.messages.main_menu_keyboard', return_value=mock_keyboard):
        result = await send_main_menu(123, mock_context)
        
        # Проверяем вызов send_message
        mock_context.bot.send_message.assert_awaited_once_with(
            chat_id=123,
            text="Добро пожаловать! Выберите действие:",
            reply_markup=mock_keyboard
        )
        assert result is True