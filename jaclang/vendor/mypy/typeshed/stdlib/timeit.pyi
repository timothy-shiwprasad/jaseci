from collections.abc import Callable, Sequence
from typing import IO, Any
from typing_extensions import TypeAlias

__all__ = ["Timer", "timeit", "repeat", "default_timer"]

_Timer: TypeAlias = Callable[[], float]
_Stmt: TypeAlias = str | Callable[[], object]

default_timer: _Timer

class Timer:
    def __init__(
        self,
        stmt: _Stmt = "pass",
        setup: _Stmt = "pass",
        timer: _Timer = ...,
        globals: dict[str, Any] | None = None,
    ) -> None: ...
    def print_exc(self, file: IO[str] | None = None) -> None: ...
    def timeit(self, number: int = 1000000) -> float: ...
    def repeat(self, repeat: int = 5, number: int = 1000000) -> list[float]: ...
    def autorange(
        self, callback: Callable[[int, float], object] | None = None
    ) -> tuple[int, float]: ...

def timeit(
    stmt: _Stmt = "pass",
    setup: _Stmt = "pass",
    timer: _Timer = ...,
    number: int = 1000000,
    globals: dict[str, Any] | None = None,
) -> float: ...
def repeat(
    stmt: _Stmt = "pass",
    setup: _Stmt = "pass",
    timer: _Timer = ...,
    repeat: int = 5,
    number: int = 1000000,
    globals: dict[str, Any] | None = None,
) -> list[float]: ...
def main(
    args: Sequence[str] | None = None,
    *,
    _wrap_timer: Callable[[_Timer], _Timer] | None = None
) -> None: ...
