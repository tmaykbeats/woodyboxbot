import pytest
from unittest.mock import patch, AsyncMock
from handlers.commands import start

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    with patch('handlers.commands.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await start(mock_update, mock_context)
        
        # Проверяем вызов главного меню
        mock_send_menu.assert_called_once_with(
            user_id=123,
            context=mock_context
        )