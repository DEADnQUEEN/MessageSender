from typing import Callable


def format_to_digits_only(text: str) -> str:
    formated = ""
    for char in text:
        if char.isdigit():
            formated += char

    return formated


def format_to_first_upper(text: str) -> str:
    return text.capitalize()


def format_to_uppercase(text: str) -> str:
    return text.upper()


FORMAT_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "upper": format_to_uppercase,
    "digits_only": format_to_digits_only,
    "capitalize": format_to_first_upper,
    "do_nothing": lambda v: v,
}
