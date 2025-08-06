from typing import Callable
from utils.config import BASE_TEXT, TEXT_REPLACES

def text_format(*content) -> str:
    text = BASE_TEXT

    for i in range(max(len(content), len(TEXT_REPLACES))):
        text = text.replace(TEXT_REPLACES[i], content[i])

    return text


def format_number(text: str) -> str:
    formated = ""
    for char in text:
        if char.isdigit():
            formated += char

    return formated


def format_city(text: str) -> str:
    return text.capitalize()


def format_code(text: str) -> str:
    return text.upper()


FORMATERS: dict[str, Callable[[str], str]] = {
    "code": format_code,
    "number": format_number,
    "city": format_city,
    "": lambda _: _,
}
