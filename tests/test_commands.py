import pytest
from unittest.mock import patch, AsyncMock
from src.handlers.commands import start
from src.handlers.callbacks import button_handler

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    with patch('src.handlers.commands.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await start(mock_update, mock_context)
        
        # Проверяем вызов главного меню с позиционными аргументами
        mock_send_menu.assert_called_once_with(123, mock_context)