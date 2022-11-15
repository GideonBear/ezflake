from __future__ import annotations

from ast import NodeVisitor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Plugin


class Visitor(NodeVisitor):
    def __init__(self, plugin: Plugin):
        super().__init__()
        self.plugin = plugin
        self.violate_node = plugin.violate_node
