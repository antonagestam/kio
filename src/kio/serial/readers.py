from __future__ import annotations

import datetime
import logging
import struct

from collections.abc import Callable
from collections.abc import Generator
from typing import Final
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar
from uuid import UUID

from typing_extensions import Buffer

from kio.schema.errors import ErrorCode
from kio.static.constants import uuid_zero
from kio.static.primitive import TZAware
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.primitive import i64Timedelta
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64

from .errors import BufferUnderflow
from .errors import OutOfBoundValue
from .errors import UnexpectedNull

logger: Final = logging.getLogger(__name__)

T = TypeVar("T")
SizedResult: TypeAlias = tuple[T, int]


class Reader(Protocol[T]):
    def __call__(
        self,
        buffer: Buffer,
        offset: int,
        /,
    ) -> SizedResult[T]: ...


def _read_exact(
    buffer: Buffer,
    offset: int,
    size: int,
) -> memoryview:
    end_offset = offset + size
    value_bytes = memoryview(buffer)[offset:end_offset]
    if len(value_bytes) < size:
        raise BufferUnderflow(
            f"Expected to read {size} bytes, only {len(value_bytes)} available "
            f"in buffer."
        )
    return value_bytes


def _take_bytes(byte_size: int) -> Callable[[Callable[[memoryview], T]], Reader[T]]:
    def decorator(reader: Callable[[memoryview], T]) -> Reader[T]:
        def wrapper(buffer: Buffer, offset: int, /) -> SizedResult[T]:
            return reader(_read_exact(buffer, offset, byte_size)), byte_size

        return wrapper

    return decorator


@_take_bytes(1)
def read_boolean(value_bytes: memoryview) -> bool:
    return struct.unpack(">?", value_bytes)[0]


@_take_bytes(1)
def read_int8(value_bytes: memoryview, /) -> i8:
    return struct.unpack(">b", value_bytes)[0]


@_take_bytes(2)
def read_int16(value_bytes: memoryview, /) -> i16:
    return struct.unpack(">h", value_bytes)[0]


@_take_bytes(4)
def read_int32(value_bytes: memoryview, /) -> i32:
    return struct.unpack(">i", value_bytes)[0]


@_take_bytes(8)
def read_int64(value_bytes: memoryview) -> i64:
    return struct.unpack(">q", value_bytes)[0]


@_take_bytes(1)
def read_uint8(value_bytes: memoryview) -> u8:
    return struct.unpack(">B", value_bytes)[0]


@_take_bytes(2)
def read_uint16(value_bytes: memoryview) -> u16:
    return struct.unpack(">H", value_bytes)[0]


@_take_bytes(4)
def read_uint32(value_bytes: memoryview) -> u32:
    return struct.unpack(">I", value_bytes)[0]


@_take_bytes(8)
def read_uint64(value_bytes: memoryview) -> u64:
    return struct.unpack(">Q", value_bytes)[0]


# See description and upstream implementation.
# https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
# https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
def read_unsigned_varint(buffer: Buffer, offset: int, /) -> SizedResult[int]:
    """Deserialize an integer stored into variable number of bytes (1-5)."""
    result = 0

    # Increase shift by 7 on each iteration, looping at most 5 times.
    for index, shift in enumerate(range(0, 4 * 7 + 1, 7)):
        # Read by a byte at a time.
        [byte] = _read_exact(buffer, offset + index, 1)
        # Add 7 least significant bits to the result.
        result |= (byte & 0b01111111) << shift
        # If the most significant bit is 1, continue. Otherwise, stop.
        if byte & 0b10000000 == 0:
            return result, index + 1
    raise ValueError(
        "Varint is too long, the most significant bit in the 5th byte is set"
    )


@_take_bytes(8)
def read_float64(value_bytes: memoryview) -> float:
    return struct.unpack(">d", value_bytes)[0]


def read_compact_string_as_bytes(buffer: Buffer, offset: int, /) -> SizedResult[bytes]:
    stored_length, length_size = read_unsigned_varint(buffer, offset)
    if stored_length == 0:
        raise UnexpectedNull(
            "Unexpectedly read null where compact string/bytes was expected"
        )
    # Apache Kafka® uses the string length plus 1.
    value_size = stored_length - 1
    value_bytes = _read_exact(
        buffer,
        offset + length_size,
        value_size,
    )
    return bytes(value_bytes), length_size + value_size


def read_compact_string_as_bytes_nullable(
    buffer: Buffer, offset: int, /
) -> SizedResult[bytes | None]:
    stored_length, length_size = read_unsigned_varint(buffer, offset)
    if stored_length == 0:
        return None, length_size
    # Apache Kafka® uses the string length plus 1.
    value_size = stored_length - 1
    value_bytes = _read_exact(
        buffer,
        offset + length_size,
        value_size,
    )
    return bytes(value_bytes), length_size + value_size


def read_compact_string(buffer: Buffer, offset: int, /) -> SizedResult[str]:
    bytes_value, size = read_compact_string_as_bytes(buffer, offset)
    return bytes_value.decode(), size


def read_compact_string_nullable(
    buffer: Buffer, offset: int, /
) -> SizedResult[str | None]:
    bytes_value, size = read_compact_string_as_bytes_nullable(buffer, offset)
    if bytes_value is None:
        return None, size
    return bytes_value.decode(), size


def read_legacy_bytes(buffer: Buffer, offset: int, /) -> SizedResult[bytes]:
    length, length_size = read_int32(buffer, offset)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where bytes was expected")
    bytes_view = _read_exact(buffer, offset + length_size, length)
    return bytes(bytes_view), length_size + length


def read_nullable_legacy_bytes(
    buffer: Buffer, offset: int, /
) -> SizedResult[bytes | None]:
    length, length_size = read_int32(buffer, offset)
    if length == -1:
        return None, length_size
    bytes_view = _read_exact(buffer, offset + length_size, length)
    return bytes(bytes_view), length_size + length


def read_legacy_string(buffer: Buffer, offset: int, /) -> SizedResult[str]:
    length, length_size = read_int16(buffer, offset)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where string/bytes was expected")
    bytes_view = _read_exact(buffer, offset + length_size, length)
    return bytes(bytes_view).decode(), length_size + length


def read_nullable_legacy_string(
    buffer: Buffer, offset: int, /
) -> SizedResult[str | None]:
    length, length_size = read_int16(buffer, offset)
    if length == -1:
        return None, length_size
    bytes_view = _read_exact(buffer, offset + length_size, length)
    return bytes(bytes_view).decode(), length_size + length


read_legacy_array_length: Final = read_int32


def read_compact_array_length(buffer: Buffer, offset: int, /) -> SizedResult[int]:
    encoded_length, size = read_unsigned_varint(buffer, offset)
    # Apache Kafka® uses the array size plus 1.
    return encoded_length - 1, size


@_take_bytes(16)
def read_uuid(value_bytes: memoryview) -> UUID | None:
    if value_bytes == uuid_zero.bytes:
        return None
    return UUID(bytes=bytes(value_bytes))


P = TypeVar("P")
Q = TypeVar("Q")


def _materialize_and_return(
    generator: Generator[P, None, Q],
) -> tuple[tuple[P, ...], Q]:
    values = []
    try:
        while True:
            values.append(next(generator))
    except StopIteration as stop:
        return tuple(values), stop.value
    else:
        raise ValueError("Generator did not raise StopIteration")


def _read_length_items(
    item_reader: Reader[T],
    length: int,
    buffer: Buffer,
    offset: int,
) -> Generator[T, None, int]:
    accumulating_offset = offset
    for _ in range(length):
        item_value, item_size = item_reader(buffer, accumulating_offset)
        accumulating_offset += item_size
        yield item_value
    return accumulating_offset - offset


def compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(
        buffer: Buffer, offset: int, /
    ) -> SizedResult[tuple[T, ...] | None]:
        length, length_size = read_compact_array_length(buffer, offset)
        if length == -1:
            return None, length_size
        items, items_size = _materialize_and_return(
            _read_length_items(item_reader, length, buffer, offset + length_size)
        )
        return items, length_size + items_size

    return read_compact_array


def legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(
        buffer: Buffer, offset: int, /
    ) -> SizedResult[tuple[T, ...] | None]:
        length, length_size = read_legacy_array_length(buffer, offset)
        if length == -1:
            return None, length_size
        items, items_size = _materialize_and_return(
            _read_length_items(item_reader, length, buffer, offset + length_size)
        )
        return items, length_size + items_size

    return read_compact_array


def read_error_code(buffer: Buffer, offset: int, /) -> SizedResult[ErrorCode]:
    error_code, size = read_int16(buffer, offset)
    return ErrorCode(error_code), size


def read_timedelta_i32(buffer: Buffer, offset: int, /) -> SizedResult[i32Timedelta]:
    milliseconds, size = read_int32(buffer, offset)
    return datetime.timedelta(milliseconds=milliseconds), size  # type: ignore[return-value]


def read_timedelta_i64(buffer: Buffer, offset: int, /) -> SizedResult[i64Timedelta]:
    milliseconds, size = read_int64(buffer, offset)
    return datetime.timedelta(milliseconds=milliseconds), size  # type: ignore[return-value]


def _tz_aware_from_i64(timestamp: i64) -> TZAware:
    dt = datetime.datetime.fromtimestamp(timestamp / 1000, datetime.UTC)
    try:
        return TZAware.truncate(dt)
    except TypeError as exception:
        raise OutOfBoundValue("Read invalid value for datetime") from exception


def read_datetime_i64(buffer: Buffer, offset: int, /) -> SizedResult[TZAware]:
    timestamp, size = read_int64(buffer, offset)
    return _tz_aware_from_i64(timestamp), size


def read_nullable_datetime_i64(
    buffer: Buffer, offset: int, /
) -> SizedResult[TZAware | None]:
    timestamp, size = read_int64(buffer, offset)
    if timestamp == -1:
        return None, size
    return _tz_aware_from_i64(timestamp), size


try:
    import _kio_core
except ImportError:
    logger.debug("No compiled _kio_core found, using pure Python implementation")
else:
    for name in _kio_core.__all__:
        imported = _kio_core.__dict__[name]
        imported.__module__ = __name__
        # fixme
        # globals()[name] = imported
