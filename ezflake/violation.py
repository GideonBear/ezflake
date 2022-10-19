from dataclasses import dataclass
from functools import partial
from typing import Type, Dict, Any

from .plugin import Plugin


@dataclass
class Violation:
    code: int
    message: str
    lineno: int
    col: int
    kwargs: Dict[str, Any]

    @property
    def full_message(self):
        return f'{self.code} {self.formatted_message}'

    @property
    def formatted_message(self):
        return self.message.format(**self.kwargs)

    def as_tuple(self, type_: Type[Plugin]):
        return self.lineno, self.col, self.full_message, type_


create_violation = partial(partial, Violation)
