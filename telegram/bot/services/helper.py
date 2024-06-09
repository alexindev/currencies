
def current_settings_text(data: dict) -> str:

    text = 'Текущие настройки:\n\n'
    long_percent = data.get('long_percent')
    short_percent = data.get('short_percent')
    long_time = data.get('long_time')
    short_time = data.get('short_time')

    if long_percent:
        text += f'Процент лонг: {long_percent}\n\n'
    if short_percent:
        text += f'Процент шорт: {short_percent}\n\n'
    if long_time:
        text += f'Время лонг: {long_time}\n\n'
    if short_time:
        text += f'Время шорт: {short_time}'
    return text
