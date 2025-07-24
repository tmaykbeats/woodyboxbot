import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from handlers.events import handle_new_members
from config import config

@pytest.mark.asyncio
async def test_new_member_event(mock_update, mock_context, monkeypatch, caplog):
    # Устанавливаем уровень логирования для захвата DEBUG
    caplog.set_level("DEBUG")
    
    # Устанавливаем ID канала
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    
    # Настраиваем чат прямо в message
    mock_update.message.chat.id = 12345
    
    # Убедимся, что бот не пропускает себя
    mock_context.bot.id = 123
    
    # Создаем нового пользователя
    new_user = MagicMock()
    new_user.id = 999
    new_user.first_name = "New"
    new_user.is_bot = False
    
    # Устанавливаем новых участников
    mock_update.message.new_chat_members = [new_user]
    
    with patch('handlers.events.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        # Запускаем обработчик
        await handle_new_members(mock_update, mock_context)
        
        # Выводим все логи
        print("\nЛоги обработчика:")
        for record in caplog.records:
            print(f"{record.levelname}: {record.message}")
        
        # Проверяем вызов
        if mock_send_menu.await_count == 0:
            print("send_main_menu не была вызвана!")
        else:
            print(f"send_main_menu вызвана {mock_send_menu.await_count} раз")
        
        # Исправлено: проверка позиционных аргументов
        mock_send_menu.assert_awaited_once_with(999, mock_context)

@pytest.mark.asyncio
async def test_new_member_wrong_channel(mock_update, mock_context, monkeypatch):
    # Устанавливаем ID канала
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    
    # Настраиваем чат с другим ID
    mock_update.message.chat.id = 54321
    
    mock_context.bot.id = 123
    new_user = MagicMock()
    new_user.id = 999
    mock_update.message.new_chat_members = [new_user]
    
    with patch('handlers.messages.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        mock_send_menu.assert_not_awaited()