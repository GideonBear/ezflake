from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type, Dict, Tuple

from .plugin import Plugin


ViolationTuple = Tuple[int, int, str, Type[Plugin]]


@dataclass
class ViolationType:
    code: str
    message: str

    def __post_init__(self) -> None:
        self.full_message = f'{self.code} {self.message}'

    def __call__(self, *args: object, **kwargs: object) -> Violation:
        return Violation(self, *args, **kwargs)


@dataclass
class Violation:
    type: ViolationType
    lineno: int
    col: int
    args: Tuple[object, ...] = ()
    kwargs: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.formatted_message = self.type.full_message.format(*self.args, **self.kwargs)

    def as_tuple(self, type_: Type[Plugin]) -> ViolationTuple:
        return self.lineno, self.col, self.formatted_message, type_
