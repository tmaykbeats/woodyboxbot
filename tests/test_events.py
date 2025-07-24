import pytest
from unittest.mock import patch, AsyncMock
from telegram import User  # Импортируем User
from handlers.events import handle_new_members

@pytest.mark.asyncio
async def test_new_member_event(mock_update, mock_context):
    # Эмулируем нового пользователя
    new_user = User(id=999, first_name="New", is_bot=False)
    mock_update.message.new_chat_members = [new_user]
    
    with patch('handlers.events.send_welcome_message', new_callable=AsyncMock) as mock_welcome:
        mock_welcome.return_value = True
        
        await handle_new_members(mock_update, mock_context)
        
        # Проверяем отправку приветствия
        mock_welcome.assert_called_once_with(
            user_id=999,
            context=mock_context
        )