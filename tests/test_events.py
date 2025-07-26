import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.handlers.events import handle_new_members
from src.config import config
from src.handlers.callbacks import button_handler

@pytest.mark.asyncio
async def test_new_member_event(mock_update: MagicMock, mock_context: MagicMock, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    mock_context.bot.id = 123
    
    new_user = MagicMock()
    new_user.id = 999
    new_user.first_name = "New"
    new_user.is_bot = False
    mock_update.message.new_chat_members = [new_user]
    
    # Убедимся, что get_chat мокирован
    mock_context.bot.get_chat = AsyncMock(return_value=MagicMock(username="test_user"))
    
    # Патчим правильный модуль (возможно нужно изменить путь)
    with patch('src.handlers.events.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        mock_send_menu.assert_awaited_once_with(999, mock_context)

@pytest.mark.asyncio
async def test_new_member_wrong_channel(mock_update: MagicMock, mock_context: MagicMock, monkeypatch: pytest.MonkeyPatch):
    # Устанавливаем ID канала
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    
    # Настраиваем чат с другим ID
    mock_update.message.chat.id = 54321
    
    mock_context.bot.id = 123
    new_user = MagicMock()
    new_user.id = 999
    mock_update.message.new_chat_members = [new_user]
    
    mock_context.bot.get_chat = AsyncMock(return_value=MagicMock(username="test_user"))

# Тест для случая, когда новый участник - это сам бот
@pytest.mark.asyncio
async def test_new_member_is_bot(mock_update, mock_context, monkeypatch, caplog):
    caplog.set_level("INFO")
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    
    # Бот добавляет самого себя
    bot_user = MagicMock()
    bot_user.id = mock_context.bot.id
    bot_user.is_bot = True
    mock_update.message.new_chat_members = [bot_user]
    
    with patch('src.handlers.messages.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        mock_send_menu.assert_not_awaited()
        assert any("Пропускаем бота" in record.message for record in caplog.records)

# Тест для случая, когда добавляется несколько участников
@pytest.mark.asyncio
async def test_multiple_new_members(mock_update, mock_context, monkeypatch):
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    
    user1 = MagicMock(id=101, first_name="User1", is_bot=False)
    user2 = MagicMock(id=102, first_name="User2", is_bot=False)
    mock_update.message.new_chat_members = [user1, user2]
    
    # Используем правильное мокирование
    mock_context.bot.get_chat = AsyncMock(return_value=MagicMock(username="test_user"))
    
    with patch('src.handlers.events.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        assert mock_send_menu.await_count == 2

@pytest.mark.asyncio
async def test_new_member_send_menu_error(mock_update, mock_context, monkeypatch, caplog):
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    mock_context.bot.id = 123
    
    new_user = MagicMock()
    new_user.id = 999
    new_user.first_name = "New"
    new_user.is_bot = False
    mock_update.message.new_chat_members = [new_user]
    
    with patch('src.handlers.events.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        mock_send_menu.side_effect = Exception("Send error")
        await handle_new_members(mock_update, mock_context)
        
        assert "Ошибка при отправке меню: Send error" in caplog.text

@pytest.mark.asyncio
async def test_multiple_bots_added(mock_update, mock_context, monkeypatch):
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    
    bot1 = MagicMock(id=101, is_bot=True)
    bot2 = MagicMock(id=102, is_bot=True)
    mock_update.message.new_chat_members = [bot1, bot2]
    
    with patch('src.handlers.events.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        mock_send_menu.assert_not_awaited()

@pytest.mark.asyncio
async def test_send_menu_error(mock_update, mock_context, monkeypatch, caplog):
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    mock_update.message.chat.id = 12345
    new_user = MagicMock(id=999, is_bot=False)
    mock_update.message.new_chat_members = [new_user]
    
    with patch('src.handlers.events.send_main_menu', AsyncMock(side_effect=Exception("Test error"))):
        await handle_new_members(mock_update, mock_context)
        assert "Ошибка при отправке меню" in caplog.text