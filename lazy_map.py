from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final
from typing import Generic
from typing import TypeVar
from typing import assert_type

from kio._utils import DataclassInstance

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class SimpleMappingDescriptor(Generic[K, V]):
    # fixme
    # __slots__ = ("_source_field",)

    def __init__(
        self,
        field_name: str,
        map_key: str,
        key_type: type[K],
        value_type: type[V],
    ) -> None:
        self._field_name: Final = field_name
        self._map_key: Final = map_key
        self._key_type: Final = key_type

    def __call__(self) -> dict[K, V]:
        source = getattr(instance, self._field_name)
        return {getattr(value, self._map_key): value for value in source}

    def __get__(
        self,
        instance: DataclassInstance,
        type_: type,
    ) -> Callable[[], dict[K, V]]:
        return self


@dataclass(frozen=True)
class E:
    k: str
    v: int


@dataclass(frozen=True)
class F:
    nested: tuple[E, ...]

    def build_nested_map(self) -> dict[str, E]:
        return {item.k: item for item in self.nested}


instance = F(
    nested=(E("a", 1), E("b", 2), E("c", 3)),
)
mapped = instance.build_nested_map()

assert_type(mapped, dict[str, E])

assert mapped == {
    "a": E("a", 1),
    "b": E("b", 2),
    "c": E("c", 3),
}
