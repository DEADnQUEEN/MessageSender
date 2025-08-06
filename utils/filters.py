from utils import config
from typing import Callable

def not_empty(value: str) -> bool:
    return len(value) != 0


def template_exists(name: str) -> bool:
    return name in config.CONFIG['templates']

FILTERS: dict[str, Callable[[str], bool]] = {
    'not_empty': not_empty,
    'template_exists': template_exists,
}
