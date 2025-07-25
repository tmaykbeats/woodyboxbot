import pytest
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture
def mock_update():
    update = MagicMock()
    
    # Настраиваем effective_user
    user = MagicMock()
    user.id = 123
    user.first_name = "Test"
    user.is_bot = False
    update.effective_user = user
    
    # Настраиваем callback_query с AsyncMock
    callback_query = AsyncMock()
    callback_query.data = None
    callback_query.edit_message_text = AsyncMock()
    update.callback_query = callback_query
    
    # Настраиваем message
    message = MagicMock()
    message.new_chat_members = []
    message.chat = MagicMock()  # Добавляем объект чата
    message.chat.id = 12345     # Устанавливаем ID по умолчанию
    
    update.message = message
    
    return update

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.bot = MagicMock()
    context.bot.username = "test_bot"
    context.bot.id = 123  # ID бота
    context.bot.send_message = AsyncMock()
    context.bot.edit_message_text = AsyncMock()
    
    # Настраиваем get_chat
    chat_user = MagicMock()
    chat_user.id = 123
    chat_user.username = "test_user"
    context.bot.get_chat = AsyncMock(return_value=chat_user)
    
    return context