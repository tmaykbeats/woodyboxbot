import os
import json
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получаем абсолютный путь к корню проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# Загрузка конфига из JSON
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Глобальные переменные
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
ADMIN_ID = os.getenv('ADMIN_ID')

# Добавляем CHANNEL_ID в config
config['CHANNEL_ID'] = CHANNEL_ID