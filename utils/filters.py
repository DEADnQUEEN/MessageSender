from utils import config
from typing import Callable


def is_not_empty(value: str) -> bool:
    return len(value) != 0


def is_template_exists(name: str) -> bool:
    return name in config.CONFIG['templates']


FILTERS: dict[str, Callable[[str], bool]] = {
    'not_empty': is_not_empty,
    'template_exists': is_template_exists,
    "do_nothing": lambda _: True,
}
