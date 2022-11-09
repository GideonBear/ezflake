from __future__ import annotations

from typing import Iterable, TypeVar

T = TypeVar('T')


def all_return(iterable: Iterable[T]) -> list[T] | bool:
    lst = []
    for item in iterable:
        if not item:
            return False
        lst.append(item)
    return lst
