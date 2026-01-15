import os
import time
import datetime
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# Загружаем переменные окружения
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = "NeuraAI Assistant"

print(f"🤖 {BOT_NAME} запускается...")
print(f"🐍 Python 3.13.7")
print(f"🔑 Токен: {TOKEN[:10]}...")

bot = Bot(token=TOKEN)

def send_message(chat_id, text):
    """Отправка сообщения"""
    try:
        bot.send_message(chat_id=chat_id, text=text)
        return True
    except TelegramError as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

def process_updates():
    """Обработка обновлений"""
    print("🔄 Проверка обновлений...")
    
    try:
        # Получаем последние обновления
        updates = bot.get_updates(timeout=30)
        
        for update in updates:
            if update.message:
                chat_id = update.message.chat_id
                text = update.message.text
                
                if text == "/start":
                    response = f"🚀 {BOT_NAME} работает на Render.com!\nВерсия: 4.0\nPython: 3.13.7"
                    send_message(chat_id, response)
                elif text:
                    response = f"📝 Вы написали: {text}\n✅ Бот работает исправно!"
                    send_message(chat_id, response)
        
        return True
    except Exception as e:
        print(f"⚠️ Ошибка обработки: {e}")
        return False

def main():
    """Основной цикл"""
    print("=" * 50)
    print(f"🤖 {BOT_NAME} - Render.com")
    print("=" * 50)
    
    # Проверяем подключение
    try:
        bot_info = bot.get_me()
        print(f"✅ Бот: @{bot_info.username}")
        print(f"✅ Имя: {bot_info.first_name}")
        print("✅ Подключение успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    print("=" * 50)
    print("🔄 Запуск основного цикла...")
    print("=" * 50)
    
    # Основной цикл
    while True:
        try:
            process_updates()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Остановка бота...")
            break
        except Exception as e:
            print(f"⚠️ Ошибка в основном цикле: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()