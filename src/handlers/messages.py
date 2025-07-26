import logging
from telegram.ext import CallbackContext
from src.handlers.keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)

async def send_main_menu(user_id: int, context: CallbackContext):
    """Отправка главного меню"""
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="Добро пожаловать! Выберите действие:",
            reply_markup=main_menu_keyboard()
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке главного меню: {e}")
        return False
    
async def test_send_main_menu_failure(mocker, caplog):
    # Создаем mock-объект для бота
    mock_bot = mocker.Mock()
    mock_bot.send_message.side_effect = Exception("Test error")
    
    with caplog.at_level(logging.ERROR):
        context = CallbackContext(bot=mock_bot)
        result = await send_main_menu(123, context)
        assert result is False
        assert "Test error" in caplog.text  # Исправлена переменная