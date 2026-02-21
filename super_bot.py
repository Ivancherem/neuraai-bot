import os
import asyncio
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Загружаем переменные окружения
load_dotenv()

# Конфигурация
TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME', 'NeuraAI Assistant')
BOT_VERSION = os.getenv('BOT_VERSION', '4.0')

# Данные о вас (ваши реальные контакты)
OWNER = {
    "name": "Иван Черемных",
    "telegram": "@ai_toolkit_partner09",
    "email": "cherem.7@yandex.ru",
    "vk": "vk.com/ai_cherem7",
    "site": "https://ai-toolkit.ru",
    "inn": "664900542343",
    "yandex_partner": "cherem-7"
}

# База промокодов с вашего сайта
PROMOCODES = [
    {
        "name": "Яндекс GPT 2.0 Pro",
        "code": "YGPT2026-3FREE",
        "description": "🔥 3 месяца бесплатного доступа к Pro версии",
        "features": [
            "Полный доступ ко всем функциям",
            "В 2 раза быстрее предыдущей версии",
            "Работает без VPN"
        ],
        "url": "https://360.yandex.ru/gpt?ref=AINEXUS2026"
    },
    {
        "name": "Kandinsky 4.0 Ultra",
        "code": "KANDY60",
        "description": "🎨 60% скидка на первый месяц подписки Ultra",
        "features": [
            "8K качество",
            "2000+ изображений в месяц",
            "Генерация в 3 раза быстрее"
        ],
        "url": "https://fusionbrain.ai/?ref=ainexus2026"
    },
    {
        "name": "Midjourney V8 Premium",
        "code": "MJV8FREE2026",
        "description": "✨ 1 месяц бесплатного доступа к Premium плану",
        "features": [
            "Фотореализм, аниме, 3D",
            "Неограниченное количество генераций",
            "8K качество"
        ],
        "url": "https://www.midjourney.com"
    },
    {
        "name": "GitHub Copilot X+",
        "code": "COPILOT40",
        "description": "💻 40% скидка на годовую подписку",
        "features": [
            "Пишет код за вас",
            "100+ языков программирования",
            "Интеграция со всеми IDE"
        ],
        "url": "https://github.com/features/copilot?ref=ainexus2026"
    },
    {
        "name": "GigaChat Pro 2026",
        "code": "GIGAPRO30",
        "description": "🏢 30 дней бесплатного доступа к бизнес-тарифу",
        "features": [
            "Максимальная безопасность",
            "Интеграции с российскими сервисами",
            "Выделенные серверы"
        ],
        "url": "https://developers.sber.ru/gigachat?ref=ainexus"
    },
    {
        "name": "ChatGPT 5 Omni",
        "code": "GPT5FREE30",
        "description": "🤖 30 дней бесплатного доступа к ChatGPT 5",
        "features": [
            "Поддержка видео, голоса, текста",
            "150+ языков",
            "В 100 раз быстрее ChatGPT 4"
        ],
        "url": "https://chat.openai.com"
    }
]

# Партнерские программы
PARTNERS = [
    {
        "name": "Яндекс.Директ",
        "rate": "20%",
        "description": "Контекстная реклама для любого бизнеса",
        "url": "https://yandex.ru/project/direct/partner/distribution/?partner=14661305",
        "color": "#fc3f1d"
    },
    {
        "name": "Яндекс.Браузер",
        "rate": "до 25%",
        "description": "Умный браузер с Алисой",
        "url": "https://browser.yandex.ru/corp/builds?refid=14628861",
        "color": "#FFCC00"
    },
    {
        "name": "Яндекс.Маркет",
        "rate": "10%",
        "description": "Покупки в маркетплейсе",
        "code": "MARKET_14628864",
        "url": "https://market.yandex.ru/partners?ref=14628864",
        "color": "#FF6B00"
    },
    {
        "name": "Reg.ru Cloud",
        "rate": "15%",
        "description": "Облачные серверы, хостинг",
        "url": "https://reg.cloud/?rlink=reflink-31250911",
        "color": "#7c3aed"
    }
]

# ==================== КОМАНДЫ БОТА ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton("🎁 Промокоды", callback_data="menu_promo")],
        [InlineKeyboardButton("🤝 Партнерки", callback_data="menu_partners")],
        [InlineKeyboardButton("👤 Контакты", callback_data="menu_contacts")],
        [InlineKeyboardButton("🌐 Наш сайт", url="https://ai-toolkit.ru")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
👋 Привет, {user.first_name}!

🤖 *{BOT_NAME} v{BOT_VERSION}*

💰 *Я помогу тебе зарабатывать на AI!*

🎁 *Что я умею:*
• Давать рабочие промокоды
• Показывать партнерские программы
• Рассказывать о заработке на AI

✨ *Нажми на кнопки ниже или введи команду:*
/promo - промокоды
/partners - партнерские программы
/support - мои контакты
/site - наш сайт с AI-инструментами

🌐 *Сайт:* https://ai-toolkit.ru
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def promo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /promo - показывает все промокоды"""
    keyboard = []
    for promo in PROMOCODES:
        keyboard.append([InlineKeyboardButton(promo["name"], callback_data=f"promo_{PROMOCODES.index(promo)}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="menu_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎁 *Выберите интересующий сервис:*\n\nНажмите на кнопку, чтобы увидеть промокод и активировать его.",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def partners_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /partners - показывает партнерские программы"""
    text = "🤝 *Партнерские программы для заработка*\n\n"
    
    for partner in PARTNERS:
        text += f"*{partner['name']}* — {partner['rate']}\n"
        text += f"_{partner['description']}_\n"
        if 'code' in partner:
            text += f"📋 *Код:* `{partner['code']}`\n"
        text += f"[🔗 Перейти]({partner['url']})\n\n"
    
    text += "🌐 *Больше на сайте:* https://ai-toolkit.ru"
    
    await update.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /support - контакты поддержки"""
    text = f"""
👨‍💼 *ПЕРСОНАЛЬНАЯ ПОДДЕРЖКА*

*ИВАН ЧЕРЕМНЫХ*
📱 Telegram: {OWNER['telegram']}
📧 Email: {OWNER['email']}
👥 VK: {OWNER['vk']}
🌐 Сайт: {OWNER['site']}

💼 *ОФИЦИАЛЬНАЯ ИНФОРМАЦИЯ:*
• Самозанятый с 2024 года
• ИНН: `{OWNER['inn']}`
• Яндекс.Дистрибуция: `{OWNER['yandex_partner']}`

🕒 *РЕЖИМ РАБОТЫ:*
Пн-Пт: 10:00-20:00 (МСК)
Сб-Вс: 12:00-18:00 (МСК)

⚡ *ОТВЕТ В ТЕЧЕНИЕ 15 МИНУТ!*
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def site_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /site - ссылка на сайт"""
    text = f"""
🌐 *НАШ САЙТ С AI-ИНСТРУМЕНТАМИ*

🚀 [AI-Toolkit.ru](https://ai-toolkit.ru)

📊 *Что там есть:*
• 4000+ нейросетей
• 1800+ промокодов
• 25+ партнерских программ
• 75,000+ пользователей

🔥 *Заходи, копируй промокоды и начинай зарабатывать!*
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = f"""
🆘 *Помощь по {BOT_NAME}*

📋 *Команды для заработка:*
/promo - Промокоды на AI-сервисы
/partners - Партнерские программы
/support - Мои контакты
/site - Наш сайт

📋 *Основные команды:*
/start - Запуск бота
/help - Это сообщение
/ping - Проверка связи
/time - Текущее время
/about - Информация о боте

💡 *Как зарабатывать:*
1. Бери промокоды из /promo
2. Регистрируйся по ссылкам
3. Получай комиссию

🌐 *Сайт:* https://ai-toolkit.ru
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

📡 *Серверное время*
"""
    await update.message.reply_text(time_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    about_text = f"""
🤖 *{BOT_NAME} v{BOT_VERSION}*

📝 *Описание:*
Помощник по AI-инструментам и промокодам

⚡ *Особенности:*
• Работает 24/7
• Актуальные промокоды
• Партнерские программы
• Связь с разработчиком

🛠 *Технологии:*
• Python 3.13.7
• python-telegram-bot 21.7
• Render.com Cloud

👨‍💻 *Разработчик:*
Иван Черемных
Telegram: @ai_toolkit_partner09

🌐 *Сайт:* https://ai-toolkit.ru
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text.lower()
    
    if "промокод" in text or "промо" in text:
        await promo_command(update, context)
    elif "партнер" in text or "заработ" in text or "деньги" in text:
        await partners_command(update, context)
    elif "сайт" in text or "каталог" in text:
        await site_command(update, context)
    elif "контакт" in text or "поддержк" in text:
        await support_command(update, context)
    else:
        response = f"""
💬 *Я не совсем понял ваш запрос.*

Попробуйте:
/promo - посмотреть промокоды
/partners - партнерские программы
/support - связаться со мной
/help - все команды

🌐 Или зайдите на наш сайт:
https://ai-toolkit.ru
"""
        await update.message.reply_text(response, parse_mode='Markdown')

# ==================== ОБРАБОТЧИКИ КНОПОК ====================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_main":
        keyboard = [
            [InlineKeyboardButton("🎁 Промокоды", callback_data="menu_promo")],
            [InlineKeyboardButton("🤝 Партнерки", callback_data="menu_partners")],
            [InlineKeyboardButton("👤 Контакты", callback_data="menu_contacts")],
            [InlineKeyboardButton("🌐 Наш сайт", url="https://ai-toolkit.ru")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "👋 *Главное меню*\n\nВыберите интересующий раздел:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data == "menu_promo":
        keyboard = []
        for i, promo in enumerate(PROMOCODES):
            keyboard.append([InlineKeyboardButton(promo["name"], callback_data=f"promo_{i}")])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="menu_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎁 *Выберите сервис:*",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("promo_"):
        index = int(query.data.replace("promo_", ""))
        promo = PROMOCODES[index]
        
        text = f"*{promo['name']}*\n\n"
        text += f"📋 *Промокод:* `{promo['code']}`\n\n"
        text += f"{promo['description']}\n\n"
        text += "*Преимущества:*\n"
        for feature in promo['features']:
            text += f"✓ {feature}\n"
        text += f"\n👉 [Активировать]({promo['url']})"
        
        keyboard = [[InlineKeyboardButton("🔙 К списку", callback_data="menu_promo")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup, disable_web_page_preview=True)
    
    elif query.data == "menu_partners":
        text = "🤝 *Партнерские программы*\n\n"
        for partner in PARTNERS:
            text += f"*{partner['name']}* — {partner['rate']}\n"
            text += f"_{partner['description']}_\n"
            if 'code' in partner:
                text += f"📋 Код: `{partner['code']}`\n"
            text += f"[Перейти]({partner['url']})\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="menu_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup, disable_web_page_preview=True)
    
    elif query.data == "menu_contacts":
        text = f"""
👨‍💼 *КОНТАКТЫ*

*ИВАН ЧЕРЕМНЫХ*
📱 Telegram: {OWNER['telegram']}
📧 Email: {OWNER['email']}
👥 VK: {OWNER['vk']}
🌐 Сайт: {OWNER['site']}

💼 *ИНН:* `{OWNER['inn']}`
📊 *Яндекс:* `{OWNER['yandex_partner']}`

🕒 *Работаем:* Пн-Пт 10-20, Сб-Вс 12-18
"""
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="menu_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

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
🤖 {BOT_NAME} v{BOT_VERSION} - ДЛЯ ЗАРАБОТКА
{'=' * 60}
🚀 Запуск на Render.com
{'=' * 60}
📅 Дата: {current_time}
👤 Владелец: Иван Черемных
📱 Telegram: @ai_toolkit_partner09
🌐 Сайт: https://ai-toolkit.ru
{'=' * 60}
✅ Токен загружен
✅ Промокодов: {len(PROMOCODES)}
✅ Партнерок: {len(PARTNERS)}
{'=' * 60}
💬 Бот готов к работе!
💰 Начинаем зарабатывать!
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
    application.add_handler(CommandHandler("promo", promo_command))
    application.add_handler(CommandHandler("partners", partners_command))
    application.add_handler(CommandHandler("support", support_command))
    application.add_handler(CommandHandler("site", site_command))
    
    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
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
