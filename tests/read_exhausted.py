from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def exhausted(with_remaining: BufferAnd[T]) -> T:
    remaining, value = with_remaining
    assert remaining == b""
    return value
