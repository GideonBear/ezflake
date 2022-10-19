from __future__ import annotations

import ast
from abc import abstractmethod, ABC
from typing import Tuple, Generator, List, Callable, Type

from .violation import Violation


class Visitor(ast.NodeVisitor):
    def __init__(self, plugin: Plugin):
        super().__init__()
        self.plugin = plugin
        self.violate = plugin.violate


class Plugin(ABC):
    @property
    @abstractmethod
    def visitors(self) -> List[Type[Visitor]]:
        ...

    def __init__(self, tree: ast.AST):
        self._tree = tree
        self.violations: List[Violation] = []

    def violate(self, violation_type: Callable[[int, int], Violation], node: ast.AST) -> None:
        violation = violation_type(node.lineno, node.col_offset)
        self.violations.append(violation)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        for visitor_type in self.visitors:
            visitor = visitor_type(self)
            visitor.visit(self._tree)

        for violation in self.violations:
            yield violation.as_tuple(self.__class__)
