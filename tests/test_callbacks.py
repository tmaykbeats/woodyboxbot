import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from handlers.callbacks import button_handler
import handlers.callbacks as callbacks_module  # Единый псевдоним для модуля
from telegram import InlineKeyboardButton

@pytest.mark.asyncio
async def test_back_button(mock_update, mock_context):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'welcome_message': "Test Welcome",
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        # Устанавливаем данные callback
        mock_update.callback_query.data = 'prices'
        await button_handler(mock_update, mock_context)
        
        # Проверяем вызов edit_message_text
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        
        # Получаем аргументы вызова
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Тест: 1000₽" in kwargs['text']
        assert "Бронирование" in kwargs['text']
        
    finally:
        # Восстановление оригинального конфига
        callbacks_module.config = original_config

# Тест для кнопки "Полезная информация"
@pytest.mark.asyncio
async def test_info_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'info_content': {"Тест": "https://example.com"},
            'services': {"Услуга": "500₽"},  # Добавляем для полноты конфига
            'booking_link': "https://booking.com",
            'booking_text': "Бронирование"
        }
        
        # Упрощаем мокирование клавиатуры
        with patch('handlers.callbacks.InlineKeyboardMarkup') as mock_markup:
            mock_markup.return_value = MagicMock(inline_keyboard=[])
            
        mock_update.callback_query.data = 'info'
        await button_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Тест: https://example.com" in kwargs['text']
        
    finally:
        callbacks_module.config = original_config

# Тест для кнопки "Назад"
@pytest.mark.asyncio
async def test_back_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'welcome_message': "Test Welcome",
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'back'
        
        # Устанавливаем ID пользователя для callback_query.from_user
        mock_update.callback_query.from_user.id = 123
        
        # Патчим send_main_menu
        with patch('handlers.callbacks.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
            await button_handler(mock_update, mock_context)
            
            # Проверяем вызов send_main_menu с правильными аргументами
            mock_send_menu.assert_awaited_once_with(123, mock_context)
            
    finally:
        callbacks_module.config = original_config

@pytest.mark.asyncio
async def test_prices_button(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'services': {"Test Service": "1000₽"},
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'prices'
        await button_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Test Service: 1000₽" in kwargs['text']
        
    finally:
        callbacks_module.config = original_config

@pytest.mark.asyncio
async def test_products_button(mock_update, mock_context):
    original_config = callbacks_module.config
    try:
        # Создаем тестовые данные для товаров
        test_products = [
            {"name": "Product 1", "url": "https://test.com/product1"},
            {"name": "Product 2", "url": "https://test.com/product2"}
        ]
        
        # Устанавливаем тестовый конфиг
        callbacks_module.config = {
            'products': test_products,
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'products'
        await button_handler(mock_update, mock_context)
        
        # Проверяем результат
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        
        # Проверяем текст сообщения
        assert "Наши товары" in kwargs['text']
        for product in test_products:
            assert product['name'] in kwargs['text']
            
        # Проверяем клавиатуру
        keyboard = kwargs['reply_markup'].inline_keyboard
        assert len(keyboard) == len(test_products) + 1  # + кнопка "Назад"
        
        # Проверяем кнопки товаров
        for i, product in enumerate(test_products):
            button = keyboard[i][0]
            assert button.text == product['name']
            assert button.url == product['url']
            
        # Проверяем кнопку "Назад"
        back_button = keyboard[-1][0]
        assert back_button.text == "⬅️ Назад"
        assert back_button.callback_data == 'back'
        
    finally:
        callbacks_module.config = original_config

@pytest.mark.asyncio
async def test_prices_button_empty_services(mock_update: MagicMock, mock_context: MagicMock):
    original_config = callbacks_module.config
    try:
        callbacks_module.config = {
            'services': {},
            'booking_link': "https://test.com",
            'booking_text': "Book Now"
        }
        
        mock_update.callback_query.data = 'prices'
        await button_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_awaited_once()
        args, kwargs = mock_update.callback_query.edit_message_text.call_args
        assert "Наши услуги" in kwargs['text']
        assert "Услуги не указаны" in kwargs['text']  # Проверяем обработку пустого списка
        
    finally:
        callbacks_module.config = original_config

@pytest.mark.asyncio
async def test_multiple_back_clicks(mock_update, mock_context):
    mock_update.callback_query.data = 'back'
    mock_update.callback_query.from_user.id = 123
    
    with patch('handlers.callbacks.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        # Первое нажатие
        await button_handler(mock_update, mock_context)
        # Второе нажатие
        await button_handler(mock_update, mock_context)
        
        assert mock_send_menu.await_count == 2

@pytest.mark.asyncio
async def test_unknown_callback(mock_update, mock_context):
    mock_update.callback_query.data = 'unknown'
    await button_handler(mock_update, mock_context)
    mock_update.callback_query.answer.assert_called()

@pytest.mark.parametrize("button, expected_text", [
    ('prices', "Наши услуги"),
    ('info', "Полезная информация"),
    ('products', "Наши товары")
])
async def test_button_texts(button, expected_text, mock_update, mock_context):
    mock_update.callback_query.data = button
    await button_handler(mock_update, mock_context)
    args, kwargs = mock_update.callback_query.edit_message_text.call_args
    assert expected_text in kwargs['text']

@pytest.mark.asyncio
async def test_back_button_text(mock_update, mock_context):
    mock_update.callback_query.data = 'back'
    mock_update.callback_query.from_user.id = 123
    
    with patch('handlers.callbacks.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await button_handler(mock_update, mock_context)
        
        # Проверяем что было отправлено новое сообщение
        mock_send_menu.assert_awaited_once()
        # Получаем позиционные аргументы
        args, _ = mock_send_menu.call_args
        # Проверяем текст в отправленном сообщении (аргумент 0 - user_id, аргумент 1 - context)
        # Нам нужно проверить что функция вызвана с правильным user_id
        assert args[0] == 123

@pytest.mark.asyncio
async def test_back_button_does_not_edit(mock_update, mock_context):
    mock_update.callback_query.data = 'back'
    await button_handler(mock_update, mock_context)
    mock_update.callback_query.edit_message_text.assert_not_called()

@pytest.mark.asyncio
async def test_back_button_calls_send_main_menu(mock_update, mock_context):
    mock_update.callback_query.data = 'back'
    mock_update.callback_query.from_user.id = 123
    
    with patch('handlers.callbacks.send_main_menu', new_callable=AsyncMock) as mock_send_menu:
        await button_handler(mock_update, mock_context)
        
        # Проверяем что send_main_menu была вызвана с правильными аргументами
        mock_send_menu.assert_awaited_once_with(123, mock_context)