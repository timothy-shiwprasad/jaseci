from _typeshed import SupportsWrite
from collections.abc import Iterator
from email.message import Message

__all__ = ["body_line_iterator", "typed_subpart_iterator", "walk"]

def body_line_iterator(msg: Message, decode: bool = False) -> Iterator[str]: ...
def typed_subpart_iterator(
    msg: Message, maintype: str = "text", subtype: str | None = None
) -> Iterator[str]: ...
def walk(self: Message) -> Iterator[Message]: ...

# We include the seemingly private function because it is documented in the stdlib documentation.
def _structure(
    msg: Message,
    fp: SupportsWrite[str] | None = None,
    level: int = 0,
    include_default: bool = False,
) -> None: ...
