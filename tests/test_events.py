import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.handlers.events import handle_new_members
from src.config import config
from src.handlers.callbacks import button_handler

@pytest.mark.asyncio
async def test_new_member_event(mock_update: MagicMock, mock_context: MagicMock, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
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
    
    with patch('src.handlers.messages.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
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
async def test_new_member_wrong_channel(mock_update: MagicMock, mock_context: MagicMock, monkeypatch: pytest.MonkeyPatch):
    # Устанавливаем ID канала
    monkeypatch.setitem(config, 'CHANNEL_ID', 12345)
    
    # Настраиваем чат с другим ID
    mock_update.message.chat.id = 54321
    
    mock_context.bot.id = 123
    new_user = MagicMock()
    new_user.id = 999
    mock_update.message.new_chat_members = [new_user]
    
    with patch('src.handlers.messages.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        mock_send_menu.assert_not_awaited()

# Тест для случая, когда новый участник - это сам бот
@pytest.mark.asyncio
async def test_new_member_is_bot(mock_update, mock_context, monkeypatch, caplog):
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
    
    with patch('src.handlers.messages.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await handle_new_members(mock_update, mock_context)
        assert mock_send_menu.call_count == 2