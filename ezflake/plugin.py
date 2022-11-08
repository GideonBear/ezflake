from __future__ import annotations

from _ast import AST
from abc import abstractmethod, ABC
from ast import NodeVisitor
from typing import List, Type, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .violation import Violation, ViolationType, ViolationTuple


class Visitor(NodeVisitor):
    def __init__(self, plugin: Plugin):
        super().__init__()
        self.plugin = plugin
        self.violate_node = plugin.violate_node


class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def visitors(self) -> List[Type[Visitor]]:
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        ...

    def __init__(self, tree: AST):
        self.tree = tree
        self.violations: List[Violation] = []

    def violate_node(self, violation_type: ViolationType, node: AST, *args: object, **kwargs: object) -> None:
        violation = violation_type(node.lineno, node.col_offset, args, kwargs)
        self.violations.append(violation)

    def get_violations(self) -> List[Violation]:
        for visitor_type in self.visitors:
            visitor = visitor_type(self)
            visitor.visit(self.tree)

        return self.violations

    def run(self) -> Iterator[ViolationTuple]:
        violations = self.get_violations()
        yield from (violation.as_tuple(self.__class__) for violation in violations)
