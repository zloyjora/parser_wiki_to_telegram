import os
from pathlib import Path

import telebot
from dotenv import load_dotenv

from telegram_bot.handlers.command_handlers import register_handlers
from telegram_bot.handlers.callback_handlers import register_callback_handlers

def main() -> None:
    try:
        load_dotenv()
        bot_token = os.getenv('TG_BOT_TOKEN')
        if not bot_token:
            print(f'Токен не обнаружен')
            return
        bot = telebot.TeleBot(bot_token)
        register_handlers(bot)
        register_callback_handlers(bot)
        print(f'Бот запущен')

        bot.polling()
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

if __name__ == "__main__":
    main()
