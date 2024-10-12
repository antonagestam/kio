from typing import TypeVar

from kio.serial.readers import BufferAnd

T = TypeVar("T")


def read_exhausted(with_remaining: BufferAnd[T]) -> T:
    remaining, value = with_remaining
    assert remaining == b""
    return value
