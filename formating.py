import re

# паттерн для поиска эмодзи в тексте
EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+"
)

# функция поиска эмодзи в тексте
# возвращает первое найденное эмодзи или None
def find_emoji(text) -> str | None:
    match = EMOJI_PATTERN.search(text)
    if match:
        return match.group(0)
    return None


# убираем эмодзи из текста
def remove_emoji(text) -> str:
    text = EMOJI_PATTERN.sub(". ", text)
    text = text.replace(" .", ".")
    while text.endswith(".") or text.endswith(" "):
        text = text[:-1]
    return text
