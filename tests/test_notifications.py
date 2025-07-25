import pytest
from unittest.mock import AsyncMock, MagicMock
from handlers.notifications import notify_user_in_channel

@pytest.mark.asyncio
async def test_notify_user_in_channel_success(mock_context):
    # Настройка моков
    mock_context.bot.get_chat = AsyncMock(return_value=MagicMock(username="test_user"))
    mock_context.bot.send_message = AsyncMock()
    
    await notify_user_in_channel(123, mock_context)
    
    mock_context.bot.send_message.assert_awaited_once()
    args, kwargs = mock_context.bot.send_message.call_args
    assert "Привет, test_user!" in kwargs['text']
    assert "Открыть бота" in kwargs['reply_markup'].inline_keyboard[0][0].text

@pytest.mark.asyncio
async def test_notify_user_in_channel_error(mock_context, caplog):
    # Эмуляция ошибки при отправке
    mock_context.bot.send_message = AsyncMock(side_effect=Exception("Test error"))
    
    await notify_user_in_channel(123, mock_context)
    
    assert "Ошибка при отправке уведомления: Test error" in caplog.text