from utils import config
from typing import Callable
import datetime

def not_empty(value: str) -> bool:
    return len(value) != 0


def template_exists(name: str) -> bool:
    return name in config.CONFIG['templates']

def exact(value: str) -> bool:
    return value == value


FILTERS: dict[str, Callable[[str], bool]] = {
    'not_empty': not_empty,
    'template_exists': template_exists,
    "exact": exact,
    "": lambda _: _,
}
