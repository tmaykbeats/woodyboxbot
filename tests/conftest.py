# tests/conftest.py
import pytest
from unittest.mock import MagicMock, AsyncMock
from telegram import User, Update, Message, Chat, CallbackQuery

@pytest.fixture
def mock_update():
    update = MagicMock(spec=Update)
    update.effective_user = User(id=123, first_name="Test", is_bot=False)
    update.callback_query = CallbackQuery(id="test_query", from_user=update.effective_user)
    update.message = Message(
        message_id=456, 
        chat=Chat(id=789, type='channel'), 
        from_user=update.effective_user
    )
    return update

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.bot = MagicMock()
    context.bot.username = "test_bot"
    context.bot.send_message = AsyncMock()
    context.bot.edit_message_text = AsyncMock()
    context.bot.get_chat = AsyncMock(return_value=User(id=123, first_name="Test"))
    return context

@pytest.fixture
def mock_user():
    return User(id=123, first_name="Test", is_bot=False)