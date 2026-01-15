import os
import asyncio
import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения
load_dotenv()

# Конфигурация
TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME', 'NeuraAI Assistant')
BOT_VERSION = os.getenv('BOT_VERSION', '4.0')

# Проверяем токен
if not TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден в переменных окружения!")
    print("ℹ️  Создайте файл .env с BOT_TOKEN=ваш_токен")
    exit(1)

# ==================== КОМАНДЫ БОТА ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = f"""
👋 Привет, {user.first_name}!

🤖 *{BOT_NAME} v{BOT_VERSION}*
🚀 Работает на Render.com 24/7

✨ *Доступные команды:*
/start - Приветствие
/help - Помощь и команды
/ping - Проверка работы бота
/time - Текущее время
/about - О боте

💡 Просто напишите мне что-нибудь!
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = f"""
🆘 *Помощь по {BOT_NAME}*

📋 *Основные команды:*
/start - Запуск бота
/help - Это сообщение
/ping - Проверка связи
/time - Текущее время
/about - Информация о боте

🔧 *Техническая информация:*
• Версия: {BOT_VERSION}
• Хостинг: Render.com
• Статус: Активен 24/7
• Дата: {datetime.datetime.now().strftime('%d.%m.%Y')}

💬 *Как пользоваться:*
Просто напишите мне сообщение, и я отвечу!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /ping"""
    start_time = datetime.datetime.now()
    message = await update.message.reply_text("🏓 Pong!...")
    end_time = datetime.datetime.now()
    response_time = (end_time - start_time).total_seconds() * 1000
    
    await message.edit_text(
        f"🏓 *Pong!*\n"
        f"⏱ Время ответа: {response_time:.2f} мс\n"
        f"🕐 Серверное время: {end_time.strftime('%H:%M:%S')}\n"
        f"📅 Дата: {end_time.strftime('%d.%m.%Y')}",
        parse_mode='Markdown'
    )

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /time"""
    current_time = datetime.datetime.now()
    time_text = f"""
🕐 *Текущее время:*

📅 *Дата:* {current_time.strftime('%d %B %Y')}
⏰ *Время:* {current_time.strftime('%H:%M:%S')}
🌍 *Часовой пояс:* UTC

📡 *Серверное время Render.com*
"""
    await update.message.reply_text(time_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    about_text = f"""
🤖 *{BOT_NAME} v{BOT_VERSION}*

📝 *Описание:*
Многофункциональный Telegram бот, работающий на облачном хостинге Render.com.

⚡ *Особенности:*
• Работает 24/7 без перерывов
• Быстрые ответы
• Простой интерфейс
• Надежный хостинг

🛠 *Технологии:*
• Python 3.13.7
• python-telegram-bot 21.7
• Render.com Cloud
• Python-dotenv

👨‍💻 *Разработчик:*
Бот создан для демонстрации работы на Render.com

🌐 *Хостинг:* https://render.com
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    
    response = f"""
💬 *Вы написали:* "{text}"

✅ Сообщение получено в {current_time}

🤖 *{BOT_NAME}* обрабатывает ваш запрос...

✨ Попробуйте команды:
/help - список всех команд
/time - текущее время
/about - информация о боте
"""
    await update.message.reply_text(response, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f"⚠️ Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Произошла ошибка при обработке запроса. Попробуйте еще раз."
        )

# ==================== ЗАПУСК БОТА ====================

def print_banner():
    """Печать баннера при запуске"""
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    banner = f"""
{'=' * 60}
🤖 {BOT_NAME} - RENDER.COM EDITION
{'=' * 60}
🚀 Запуск {BOT_NAME} на Render.com
{'=' * 60}
📅 Дата: {current_time}
⚡ Версия: {BOT_VERSION}
🐍 Python: 3.13.7
🌐 Хостинг: Render.com (Free Tier)
{'=' * 60}
✅ Токен бота загружен
✅ Библиотеки инициализированы
✅ Бот готов к работе
{'=' * 60}
📲 Telegram бот запущен
💬 Напишите /start в Telegram
{'=' * 60}
⚡ Бот работает 24/7 без вашего компьютера!
{'=' * 60}
"""
    print(banner)

async def main():
    """Основная функция запуска бота"""
    print_banner()
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🔍 Проверка соединения с Telegram API...")
    try:
        await application.initialize()
        await application.start()
        bot_info = await application.bot.get_me()
        print(f"✅ Бот подключен: @{bot_info.username}")
        print(f"✅ Имя бота: {bot_info.first_name}")
        print(f"✅ ID бота: {bot_info.id}")
        
        print("\n" + "=" * 60)
        print("🔄 Запуск polling...")
        print("=" * 60)
        
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Бесконечный цикл
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        await application.stop()
        raise

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())