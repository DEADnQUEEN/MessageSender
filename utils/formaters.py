from typing import Callable

city_to_actions = {
    "Ставрополь": "Сборка мебели",
    "Сочи": "Грузоперевозки\nСборка мебели",
    "Ростов": "Сборка мебели",
    "Новороссийск": "Сборка мебели\nУстановка дверей",
    "Краснодар": "Грузоперевозки\nАренда спецтехники\nСборка мебели\nУстановка дверей",
}


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


def format_to_city_actions(text: str) -> str:
    if text not in city_to_actions:
        raise ValueError(text)

    return city_to_actions[text]


FORMAT_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "upper": format_to_uppercase,
    "digits_only": format_to_digits_only,
    "capitalize": format_to_first_upper,
    "do_nothing": lambda v: v,
    "convert_to_action": format_to_city_actions,
}
