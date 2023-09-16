"""Jac Symbol Table."""
from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import jaclang.jac.absyntree as ast


class SymbolHitType(Enum):
    """Symbol types."""

    DECL = "decl"
    DEFN = "defn"
    USE = "use"


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        typ: Optional[type] = None,
        decl: Optional[ast.AstNode] = None,
        defn: Optional[list[ast.AstNode]] = None,
        uses: Optional[list[ast.AstNode]] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.decl = decl
        self.defn: list[ast.AstNode] = defn if defn else []
        self.uses: list[ast.AstNode] = uses if uses else []


class SymbolTable:
    """Symbol Table."""

    def __init__(self, parent: Optional[SymbolTable] = None) -> None:
        """Initialize."""
        self.parent = parent if parent else self
        self.tab: dict[str, Symbol] = {}

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        if deep and self.parent:
            return self.parent.lookup(name, deep)
        return None

    def insert(
        self,
        name: str,
        sym_hit: SymbolHitType,
        node: ast.AstNode,
        single: bool = False,
    ) -> Optional[ast.AstNode]:
        """Set a variable in the symbol table.

        Returns original symbol single check fails.
        """
        if single:
            if (
                sym_hit == SymbolHitType.DECL
                and name in self.tab
                and self.tab[name].decl
            ):
                return self.tab[name].decl
            elif (
                sym_hit == SymbolHitType.DEFN
                and name in self.tab
                and len(self.tab[name].defn)
            ):
                return self.tab[name].defn[-1]
            elif (
                sym_hit == SymbolHitType.USE
                and name in self.tab
                and len(self.tab[name].uses)
            ):
                return self.tab[name].uses[-1]
        if name not in self.tab:
            self.tab[name] = Symbol(name=name)
        if sym_hit == SymbolHitType.DECL:
            self.tab[name].decl = node
        elif sym_hit == SymbolHitType.DEFN:
            self.tab[name].defn.append(node)
        elif sym_hit == SymbolHitType.USE:
            self.tab[name].uses.append(node)

    def push_scope(self) -> SymbolTable:
        """Push a new scope onto the symbol table."""
        return SymbolTable(self)
