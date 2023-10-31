import sys
from _typeshed import StrOrBytesPath
from importlib.abc import ResourceReader
from importlib.machinery import ModuleSpec
from types import CodeType, ModuleType

if sys.version_info >= (3, 8):
    __all__ = ["ZipImportError", "zipimporter"]

class ZipImportError(ImportError): ...

class zipimporter:
    archive: str
    prefix: str
    if sys.version_info >= (3, 11):
        def __init__(self, path: str) -> None: ...
    else:
        def __init__(self, path: StrOrBytesPath) -> None: ...

    if sys.version_info < (3, 12):
        def find_loader(
            self, fullname: str, path: str | None = None
        ) -> tuple[zipimporter | None, list[str]]: ...  # undocumented
        def find_module(
            self, fullname: str, path: str | None = None
        ) -> zipimporter | None: ...

    def get_code(self, fullname: str) -> CodeType: ...
    def get_data(self, pathname: str) -> bytes: ...
    def get_filename(self, fullname: str) -> str: ...
    def get_resource_reader(
        self, fullname: str
    ) -> ResourceReader | None: ...  # undocumented
    def get_source(self, fullname: str) -> str | None: ...
    def is_package(self, fullname: str) -> bool: ...
    def load_module(self, fullname: str) -> ModuleType: ...
    if sys.version_info >= (3, 10):
        def find_spec(
            self, fullname: str, target: ModuleType | None = None
        ) -> ModuleSpec | None: ...
        def invalidate_caches(self) -> None: ...
