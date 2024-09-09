import ast as ast3
from _typeshed import Incomplete
from dataclasses import dataclass
from jaclang.compiler.absyntree import Token as Token
from jaclang.vendor.mypy.nodes import Node as MypyNode

@dataclass
class CodeGenTarget:
    py: str = ...
    jac: str = ...
    py_ast: list[ast3.AST] = ...
    mypy_ast: list[MypyNode] = ...
    py_bytecode: bytes | None = ...
    def clean(self) -> None: ...
    def __init__(
        self, py=..., jac=..., py_ast=..., mypy_ast=..., py_bytecode=...
    ) -> None: ...

class CodeLocInfo:
    first_tok: Incomplete
    last_tok: Incomplete
    def __init__(self, first_tok: Token, last_tok: Token) -> None: ...
    @property
    def mod_path(self) -> str: ...
    @property
    def first_line(self) -> int: ...
    @property
    def last_line(self) -> int: ...
    @property
    def col_start(self) -> int: ...
    @property
    def col_end(self) -> int: ...
    @property
    def pos_start(self) -> int: ...
    @property
    def pos_end(self) -> int: ...
    @property
    def tok_range(self) -> tuple[Token, Token]: ...
    @property
    def first_token(self) -> Token: ...
    @property
    def last_token(self) -> Token: ...
    def update_token_range(self, first_tok: Token, last_tok: Token) -> None: ...
    def update_first_token(self, first_tok: Token) -> None: ...
    def update_last_token(self, last_tok: Token) -> None: ...