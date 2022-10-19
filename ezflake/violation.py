from dataclasses import dataclass
from functools import partial
from typing import Type

from .plugin import Plugin


@dataclass
class Violation:
    code: int
    message: str
    lineno: int
    col: int

    def get_message(self):
        return f'{self.code} {self.message}'

    def as_tuple(self, type_: Type[Plugin]):
        return self.lineno, self.col, self.get_message(), type_


create_violation = partial(partial, Violation)
