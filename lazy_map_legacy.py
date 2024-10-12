from __future__ import annotations
from typing import Mapping, TypeVar, Final, Iterator, Sequence, TypeAlias, \
    Callable, Generic, ClassVar
from dataclasses import dataclass, field, Field
import operator

from kio._utils import DataclassInstance

T = TypeVar("T")


def t_mapper(t: type[T], mapper: Mapper[object, object]) -> Mapper[object, T]:
    def map_t(value: object) -> T:
        key = mapper(value)
        if not isinstance(key, t):
            raise ValueError(
                f"Value mapped by {mapper.__qualname__} did not return value of type "
                f"{t.__qualname__}")
        return key
    return map_t


K = TypeVar("K")
V = TypeVar("V")
Mapper: TypeAlias = Callable[[V], K]


class LazyMapView(Mapping[K, V]):
    """
    ### Examples

    >>> @dataclass(frozen=True)
    ... class E:
    ...     k: str
    ...     v: int
    >>> items = [E("a", 1), E("b", 2), E("c", 3)]
    >>> lm = LazyMapView(items, t_mapper(int, operator.attrgetter("v")))
    >>> lm[1]
    E(k='a', v=1)

    Length is determined by the underlying sequence and does not require
    materializing a dict.

    >>> len(lm)
    3

    Just like any mapping, missing keys raises KeyError.

    >>> lm["a"]
    Traceback (most recent call last):
      ...
    KeyError: 'a'

    Mapping with a different key type.

    >>> lm = LazyMapView(items, t_mapper(str, operator.attrgetter("k")))
    >>> lm["a"]
    E(k='a', v=1)

    Since LazyMapView is a Mapping, it can be converted to a dict.

    >>> dict(lm)
    {'a': E(k='a', v=1), 'b': E(k='b', v=2), 'c': E(k='c', v=3)}
    """
    __slots__ = ("_mapper", "_source", "_iter", "_materialized")

    def __init__(
        self,
        source: Sequence[V],
        mapper: Mapper[V, K],
    ) -> None:
        self._mapper: Final = mapper
        self._source: Final = source
        self._iter: Final = iter(source)
        self._materialized: dict[K, V] | None = None

    def _consume(self) -> Iterator[tuple[K, V]]:
        for value in self._iter:
            key = self._mapper(value)

            # Handling the type error means no branching and zero cost in
            # the majority of cases.
            try:
                self._materialized[key] = value  # type: ignore[index]
            except TypeError:
                if self._materialized is None:
                    self._materialized = {key: value}
                else:
                    raise

            yield key, value

    def __getitem__(self, item: K) -> V:
        # Handling the type error means no branching and zero cost in
        # the majority of cases.
        try:
            return self._materialized[item]  # type: ignore[index]
        except KeyError:
            pass
        except TypeError:
            if self._materialized is not None:
                raise

        for key, value in self._consume():
            if key == item:
                return value
        else:
            raise KeyError(item)

    def __len__(self) -> int:
        return len(self._source)

    def __iter__(self) -> Iterator[K]:
        if self._materialized is not None:
            yield from self._materialized
        for key, _ in self._consume():
            yield key

class MappingDescriptor(Generic[K, V]):
    __slots__ = ("_field_name", "_map_key", "_key_type")

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

    def __get__(
        self,
        instance: object,
        type_: type,
    ) -> Callable[[], LazyMapView[K, V]]:
        source = getattr(instance, self._field_name)
        mapper = t_mapper(self._key_type, operator.attrgetter(self._map_key))
        return lambda: LazyMapView(source, mapper)


class SimpleMappingDescriptor(Generic[K, V]):
    # __slots__ = ("_field_name", "_map_key", "_key_type")

    def __init__(
        self,
        field: Field[V],
        # field_name: str,
        # key_type: type[K],
        # value_type: type[V],
    ) -> None:
        self._source_field: Final = field
        # self._field_name: Final = field_name
        # self._map_key: Final = map_key
        # self._key_type: Final = key_type

    def __get__(
        self,
        instance: DataclassInstance | None,
        type_: type,
    ) -> Callable[[], dict[K, V]]:
        assert isinstance(instance, F), type(instance)


        def build_map() -> dict[K, V]:
            source = getattr(instance, self._source_field.name)
            return {
                getattr(value, self._source_field.metadata["map_key"]): value
                for value in source
            }
        return build_map

@dataclass(frozen=True)
class E:
    k: str
    v: int


@dataclass(frozen=True)
class F:
    nested: tuple[E, ...] = field(
        metadata={"map_key": "k"},
    )
    build_nested_map: Callable[[], dict[str, E]] = field(
        default=SimpleMappingDescriptor(
            field=nested,
            # key_type=str,
            # value_type=E,
        ),
        repr=False,
        init=False,
    )


instance = F(
    nested=(E("a", 1), E("b", 2), E("c", 3)),
)
mapped = instance.build_nested_map()

breakpoint()
