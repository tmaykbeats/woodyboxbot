import os
import json
import logging
from dotenv import load_dotenv
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

# Загрузка конфигов
load_dotenv()
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Глобальные переменные
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Конвертируем в число
ADMIN_ID = os.getenv('ADMIN_ID')

def main_menu_keyboard():
    """Клавиатура главного меню"""
    keyboard = [
        [InlineKeyboardButton("💰 Прайс-лист", callback_data='prices')],
        [InlineKeyboardButton("ℹ️ Полезная информация", callback_data='info')],
        [InlineKeyboardButton("📞 Связаться с нами", url=config['booking_link'])]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start"""
    logger.debug(f"Получена команда /start от пользователя {update.effective_user.id}")
    
    user = update.effective_user
    try:
        await update.message.reply_text(
            "Привет! Я помощник студии WoodyBox Rec.\nВыберите действие:",
            reply_markup=main_menu_keyboard()
        )
        logger.info(f"Ответ на /start отправлен пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")

async def send_welcome_message(user_id: int, context: CallbackContext):
    """Отправка приветственного сообщения с обработкой ошибок"""
    try:
        logger.info(f"Попытка отправить приветствие пользователю {user_id}")
        await context.bot.send_message(
            chat_id=user_id,
            text=config['welcome_message'],
            reply_markup=main_menu_keyboard()
        )
        logger.info(f"Приветствие отправлено пользователю {user_id}")
        return True
    except telegram.error.Forbidden as e:
        error_message = str(e).lower()
        if "bot was blocked by the user" in error_message:
            logger.warning(f"Пользователь {user_id} заблокировал бота")
        elif "user not found" in error_message or "user has not started conversation with the bot" in error_message:
            logger.info(f"У пользователя {user_id} закрыты ЛС для ботов")
            await notify_user_in_channel(user_id, context)
        return False
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")
        return False

async def notify_user_in_channel(user_id: int, context: CallbackContext):
    """Уведомление пользователя в канале о попытке связи"""
    try:
        logger.info(f"Отправка уведомления в канал для пользователя {user_id}")
        
        # Формируем текст сообщения
        text = (
            "Привет! Основатель WoodyBoxRec пытался отправить вам важное сообщение.\n\n"
            "Пожалуйста, выполните следующие шаги:\n"
            "1. Перейдите в [Настройки конфиденциальности](https://t.me/settings/privacy)\n"
            "2. В разделе 'Группы и каналы' выберите 'Кто может приглашать меня в группы и каналы?'\n"
            "3. Установите 'Все'\n\n"
            "После этого нажмите кнопку ниже, чтобы получить сообщение:"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Получить приветственное сообщение", 
                                 url=f"https://t.me/{context.bot.username}?start=welcome")]
        ])
        
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        logger.info(f"Уведомление для пользователя {user_id} отправлено в канал")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в канал: {e}")

async def handle_new_members(update: Update, context: CallbackContext) -> None:
    """Обработка новых участников канала"""
    try:
        logger.info(f"Получено обновление: {update}")
        logger.info(f"Новые участники: {update.message.new_chat_members}")
        
        # Для каждого нового участника
        for member in update.message.new_chat_members:
            logger.info(f"Новый участник: {member.id} ({member.username})")
            
            # Игнорируем, если это сам бот
            if member.id == context.bot.id:
                logger.info("Бот добавлен в канал")
                await update.message.reply_text("Бот активирован! Ожидаю новых участников.")
                continue
                
            # Пытаемся отправить приветственное сообщение
            await send_welcome_message(member.id, context)
            
    except Exception as e:
        logger.error(f"Ошибка обработки новых участников: {e}")

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == 'prices':
        services = "\n".join([f"- {s}: {p}" for s, p in config['services'].items()])
        await query.edit_message_text(
            text=f"🎹 Наши услуги:\n{services}\n\n{config['booking_text']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📅 Забронировать", url=config['booking_link'])]
            ])
        )
    
    elif query.data == 'info':
        info = "\n".join([f"• {k}: {v}" for k, v in config['info_content'].items()])
        await query.edit_message_text(
            text=f"📚 Полезные материалы:\n\n{info}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("← Назад", callback_data='back')]
            ])
        )
    
    elif query.data == 'back':
        await query.edit_message_text(
            text="Выберите действие:",
            reply_markup=main_menu_keyboard()
        )

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Логирование ошибок"""
    logger.error(msg="Ошибка обработки запроса:", exc_info=context.error)

async def test(update: Update, context: CallbackContext):
    """Тестовая команда для проверки отправки сообщений"""
    user_id = update.effective_user.id
    await send_welcome_message(user_id, context)

def main() -> None:
    """Запуск бота"""
    try:
        logger.info("Запуск бота...")
        application = Application.builder().token(BOT_TOKEN).build()

        # Обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("test", test))  # Добавлено здесь
        
        # Обработка новых участников канала - ИСПРАВЛЕННЫЙ ФИЛЬТР
        application.add_handler(MessageHandler(
            filters.Chat(chat_id=CHANNEL_ID) & filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_new_members
        ))
        
        # Обработка кнопок
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Обработка ошибок
        application.add_error_handler(error_handler)

        # Запуск бота
        logger.info("Бот успешно инициализирован")
        application.run_polling()
        logger.info("Бот запущен и работает...")
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()