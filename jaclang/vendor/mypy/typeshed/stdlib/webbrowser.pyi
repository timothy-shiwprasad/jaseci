import sys
from abc import abstractmethod
from collections.abc import Callable, Sequence
from typing_extensions import Literal

__all__ = ["Error", "open", "open_new", "open_new_tab", "get", "register"]

class Error(Exception): ...

def register(
    name: str,
    klass: Callable[[], BaseBrowser] | None,
    instance: BaseBrowser | None = None,
    *,
    preferred: bool = False
) -> None: ...
def get(using: str | None = None) -> BaseBrowser: ...
def open(url: str, new: int = 0, autoraise: bool = True) -> bool: ...
def open_new(url: str) -> bool: ...
def open_new_tab(url: str) -> bool: ...

class BaseBrowser:
    args: list[str]
    name: str
    basename: str
    def __init__(self, name: str = "") -> None: ...
    @abstractmethod
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...
    def open_new(self, url: str) -> bool: ...
    def open_new_tab(self, url: str) -> bool: ...

class GenericBrowser(BaseBrowser):
    def __init__(self, name: str | Sequence[str]) -> None: ...
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

class BackgroundBrowser(GenericBrowser): ...

class UnixBrowser(BaseBrowser):
    def open(self, url: str, new: Literal[0, 1, 2] = 0, autoraise: bool = True) -> bool: ...  # type: ignore[override]
    raise_opts: list[str] | None
    background: bool
    redirect_stdout: bool
    remote_args: list[str]
    remote_action: str
    remote_action_newwin: str
    remote_action_newtab: str

class Mozilla(UnixBrowser): ...

if sys.version_info < (3, 12):
    class Galeon(UnixBrowser):
        raise_opts: list[str]

    class Grail(BaseBrowser):
        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

class Chrome(UnixBrowser): ...
class Opera(UnixBrowser): ...
class Elinks(UnixBrowser): ...

class Konqueror(BaseBrowser):
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

if sys.platform == "win32":
    class WindowsDefault(BaseBrowser):
        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

if sys.platform == "darwin":
    class MacOSX(BaseBrowser):
        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

    class MacOSXOSAScript(
        BaseBrowser
    ):  # In runtime this class does not have `name` and `basename`
        if sys.version_info >= (3, 11):
            def __init__(self, name: str = "default") -> None: ...
        else:
            def __init__(self, name: str) -> None: ...

        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...
