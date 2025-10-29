import requests
from smart_handbook.api_clients.wikipedia_client import WikipediaClient
from telegram_bot.state import get_user_state, update_user_state
from telebot import types

wikipedia_client = WikipediaClient()

def register_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.send_message(message.chat.id, "Привет! Я Умный Справочник. \
        Чтобы получить определение, используйте команду /wiki \
        <термин>. Например: /wiki Интеграл")    

    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.send_message(message.chat.id, 'Я могу найти краткое определение\
        по любому термину из Wikipedia.Просто используйте \
        команду /wiki <термин>.\nПример: /wiki Эйлер')

    

    @bot.message_handler(commands=['wiki'])
    def wiki_command(message):
        text = message.text.split(maxsplit = 1)
        if len(text) < 2:
            bot.send_message(message.chat.id, 'Пожалуйста, укажите термин для поиска. Например: /wiki Интеграл')
            return
        try:
            response = wikipedia_client.get_summary(text[1]) 
            if response:
                chat_id = message.chat.id
                full_text = _cut(wikipedia_client.get_full_article(text[1]))
                article_url = wikipedia_client.get_article_url(text[1])

                state = get_user_state(chat_id)
                update_user_state(chat_id, article_url = article_url)

                markup = _keyboard(state)

                last_message_id = bot.send_message(chat_id, response, reply_markup = markup).message_id

                update_user_state(
                    chat_id,
                    last_term = text[1],
                    display_mode = 'summary',
                    summary_text = response,
                    full_text = full_text,
                    article_url = article_url,
                    last_message_id = last_message_id
                )



            else:
                bot.send_message(message.chat.id, f"Термин '{text[1]}' не найден в Wikipedia.")
        except requests.exceptions.Timeout as e:
            bot.send_message(message.chat.id, f'Время ожидания превышено: {e}')
            return None
        except requests.exceptions.ConnectionError as e:
            bot.send_message(message.chat.id, f'Ошибка подключения: {e}')
            return None
        except requests.exceptions.HTTPError as e:
            bot.send_message(message.chat.id, f'Ошибка сервера: {e}')
            return None
        except requests.exceptions.RequestException as e:
            bot.send_message(message.chat.id, f'Ошибка при обращении к сервису.')
            return None
        except ValueError as e:
            bot.send_message(message.chat.id, f'Ошибка значения: {e}')
            return None
        except Exception as e:
            bot.send_message(message.chat.id, f'Непредвиденная ошибка: {e}')
            return None

    @bot.message_handler(func=lambda message: message.text.startswith('/'))
    def unknown_command(message):
        bot.send_message(message.chat.id, 'Неизвестная команда. Используйте /wiki <термин>.')



def _cut(text: str | None) -> str:
    MAX_LEN = 3900
    if text:
        text = text[:MAX_LEN] + "…" if len(text) > MAX_LEN else text
    return text


def _keyboard(state: dict) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    mode = state.get('display_mode')
    if mode == 'summary':
        key1 = types.InlineKeyboardButton('Подробнее', callback_data='wiki:full')
        markup.add(key1)
    elif mode == 'full':
        key2 = types.InlineKeyboardButton('Кратко', callback_data='wiki:summary')
        markup.add(key2)

    if state.get('article_url'):
        key3 = types.InlineKeyboardButton('Читать в Wikipedia', url = state.get('article_url'))
        markup.add(key3)
    return markup
