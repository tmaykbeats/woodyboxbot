from handlers.keyboards import main_menu_keyboard, back_to_menu_keyboard, booking_keyboard

def test_main_menu_keyboard():
    keyboard = main_menu_keyboard()
    buttons = keyboard.inline_keyboard

    assert len(buttons) == 4
    assert buttons[0][0].text == "💰 Прайс-лист"
    assert buttons[1][0].text == "ℹ️ Полезная информация"
    assert buttons[2][0].text == "🛒 Товары"
    assert buttons[3][0].text == "📞 Связаться с нами"

def test_back_to_menu_keyboard():
    keyboard = back_to_menu_keyboard()
    buttons = keyboard.inline_keyboard
    
    assert len(buttons) == 1
    assert buttons[0][0].text == "← Назад"

def test_booking_keyboard():
    keyboard = booking_keyboard()
    buttons = keyboard.inline_keyboard
    
    assert len(buttons) == 1
    assert buttons[0][0].text == "📅 Забронировать"