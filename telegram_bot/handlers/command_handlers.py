import requests
from smart_handbook.api_clients.wikipedia_client import WikipediaClient

# Создаём экземпляр клиента Wikipedia
wikipedia_client = WikipediaClient()


def register_handlers(bot):
    """
    Регистрирует все обработчики команд для бота.
    
    Args:
        bot: Экземпляр telebot.Tele
    
    TODO:
        Реализуй все обработчики команд внутри этой функции.
        Используй декораторы @bot.message_handler() для регистрации.
    """
    
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
                bot.send_message(message.chat.id, response)
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
        except requests.exceptions.V as e:
            bot.send_message(message.chat.id, f'Ошибка при обращении к сервису.')
            return None
        except Exception as e:
            bot.send_message(message.chat.id, f'Непредвиденная ошибка: {e}')
            return None
        """
        Обработчик команды /wiki.
        а
        TODO:
            1. Извлеки термин
            2. Если термин не указан:
               - Отправь подсказку: "Пожалуйста, укажите термин для поиска..."
            3. Получи термин
            4. Вызови wikipedia_client.get_summary(term, lang="ru") в блоке try/except:
               - Если summary не None -> отправь его пользователю
               - Если summary == None -> отправь "Термин '{term}' не найден в Wikipedia."
            5. Обработай исключения
        """
    
    @bot.message_handler(func=lambda message: message.text.startswith('/'))
    def unknown_command(message):
        bot.send_message(message.chat.id, 'Неизвестная команда. Используйте /wiki <термин>.')
        """
        Обработчик неизвестных команд (любая команда, начинающаяся с /).

        TODO:
            Отправь сообщение: "Неизвестная команда. Используйте /wiki <термин>."
        """
