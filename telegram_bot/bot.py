import os
from pathlib import Path

import telebot
from dotenv import load_dotenv

from telegram_bot.handlers.command_handlers import register_handlers


def main() -> None:
    try:
        load_dotenv()
        TOKEN = os.getenv('TOKEN')
        if not TOKEN:
            print(f'Токен не обнаружен')
            return
        bot = telebot.TeleBot(TOKEN)
        register_handlers(bot)
        print(f'Бот запущен')

        bot.polling()
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

if __name__ == "__main__":
    main()
