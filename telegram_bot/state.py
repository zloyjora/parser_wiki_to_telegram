user_states = {}


def get_user_state(chat_id: int) -> dict:
    if chat_id not in user_states:
        user_states[chat_id] = {
           'last_term': None,
           'display_mode': 'summary',  # или 'full'
           'summary_text': None,
           'full_text': None,
           'article_url': None,
           'last_message_id': None
       }
    return user_states[chat_id]


def update_user_state(chat_id: int, **kwargs) -> None:
        if chat_id in user_states:
            user_states[chat_id].update(kwargs)


def clear_user_state(chat_id: int) -> None:
    if chat_id in user_states:
        del user_states[chat_id]
