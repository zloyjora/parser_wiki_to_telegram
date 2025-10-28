from urllib.parse import quote

import requests
from telebot import types

from smart_handbook.api_clients.wikipedia_client import WikipediaClient
from telegram_bot.handlers.command_handlers import _cut, _keyboard
from telegram_bot.state import get_user_state, update_user_state

wikipedia_client = WikipediaClient()

def register_callback_handlers(bot):
    """
    Регистрирует обработчики callback-запросов для бота.
    
    Args:
        bot: Экземпляр telebot.TeleBot
    """
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('wiki:'))
    def handle_wiki_callback(call):
        """Обработчик callback-запросов для кнопок Wikipedia."""
        # TODO:
        # 1. Подтверди получение callback
        # 2. Получи данные о сообщении, chat id, id сообщения и состояние пользователя
        # 3. Проверь, что редактируем правильное сообщение
        # 4. Проверь действие
        # 5. Переключи режим
        # 6. Обнови состояние
        # 7. Отредактируй сообщение
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        state = get_user_state(chat_id)

        if state.get('last_message_id') != message_id:
            bot.answer_callback_query(call.id, "Истекло состояние")

        
        pass  # Замени на свою реализацию