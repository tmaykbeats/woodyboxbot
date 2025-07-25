import os
import json
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Загрузка конфига из JSON
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Глобальные переменные
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Конвертируем в число
ADMIN_ID = os.getenv('ADMIN_ID')

# Добавляем CHANNEL_ID в config для использования в других модулях
config['CHANNEL_ID'] = CHANNEL_ID