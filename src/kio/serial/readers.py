from __future__ import annotations

import datetime
import struct

from collections.abc import Callable
from collections.abc import Generator
from typing import Final
from typing import TypeAlias
from typing import TypeVar
from uuid import UUID

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

T = TypeVar("T")
BufferAnd: TypeAlias = tuple[memoryview, T]
Reader: TypeAlias = Callable[[memoryview], BufferAnd[T]]


def read_exact(
    buffer: memoryview,
    num_bytes: int,
) -> BufferAnd[memoryview]:
    value_bytes = buffer[:num_bytes]
    if len(value_bytes) < num_bytes:
        raise BufferUnderflow(
            f"Expected to read {num_bytes} bytes, only {len(value_bytes)} left in "
            f"buffer."
        )
    return buffer[num_bytes:], value_bytes


def read_boolean(buffer: memoryview) -> BufferAnd[bool]:
    remaining, value_byte = read_exact(buffer, 1)
    return remaining, struct.unpack(">?", value_byte)[0]


def read_int8(buffer: memoryview) -> BufferAnd[i8]:
    remaining, value_byte = read_exact(buffer, 1)
    return remaining, struct.unpack(">b", value_byte)[0]


def read_int16(buffer: memoryview) -> BufferAnd[i16]:
    remaining, value_bytes = read_exact(buffer, 2)
    return remaining, struct.unpack(">h", value_bytes)[0]


def read_int32(buffer: memoryview) -> BufferAnd[i32]:
    remaining, value_bytes = read_exact(buffer, 4)
    return remaining, struct.unpack(">i", value_bytes)[0]


def read_int64(buffer: memoryview) -> BufferAnd[i64]:
    remaining, value_bytes = read_exact(buffer, 8)
    return remaining, struct.unpack(">q", value_bytes)[0]


def read_uint8(buffer: memoryview) -> BufferAnd[u8]:
    remaining, value_byte = read_exact(buffer, 1)
    return remaining, struct.unpack(">B", value_byte)[0]


def read_uint16(buffer: memoryview) -> BufferAnd[u16]:
    remaining, value_bytes = read_exact(buffer, 2)
    return remaining, struct.unpack(">H", value_bytes)[0]


def read_uint32(buffer: memoryview) -> BufferAnd[u32]:
    remaining, value_bytes = read_exact(buffer, 4)
    return remaining, struct.unpack(">I", value_bytes)[0]


def read_uint64(buffer: memoryview) -> BufferAnd[u64]:
    remaining, value_bytes = read_exact(buffer, 8)
    return remaining, struct.unpack(">Q", value_bytes)[0]


# See description and upstream implementation.
# https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
# https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
def read_unsigned_varint(buffer: memoryview) -> BufferAnd[int]:
    """Deserialize an integer stored into variable number of bytes (1-5)."""
    result = 0
    remaining = buffer
    # Increase shift by 7 on each iteration, looping at most 5 times.
    for shift in range(0, 4 * 7 + 1, 7):
        # Read value by a byte at a time.
        remaining, [byte] = read_exact(remaining, 1)
        # Add 7 least significant bits to the result.
        seven_bit_chunk = byte & 0b01111111
        result |= seven_bit_chunk << shift
        # If the most significant bit is 1, continue. Otherwise, stop.
        if byte & 0b10000000 == 0:
            return remaining, result
    raise ValueError(
        "Varint is too long, the most significant bit in the 5th byte is set"
    )


def read_float64(buffer: memoryview) -> BufferAnd[float]:
    remaining, value_bytes = read_exact(buffer, 8)
    return remaining, struct.unpack(">d", value_bytes)[0]


def read_compact_string_as_bytes(buffer: memoryview) -> BufferAnd[bytes]:
    remaining, length = read_unsigned_varint(buffer)
    if length == 0:
        raise UnexpectedNull(
            "Unexpectedly read null where compact string/bytes was expected"
        )
    # Apache Kafka® uses the string length plus 1.
    remaining, value_bytes = read_exact(remaining, length - 1)
    return remaining, bytes(value_bytes)


def read_compact_string_as_bytes_nullable(
    buffer: memoryview,
) -> BufferAnd[bytes | None]:
    remaining, length = read_unsigned_varint(buffer)
    if length == 0:
        return remaining, None
    # Apache Kafka® uses the string length plus 1.
    remaining, value_bytes = read_exact(remaining, length - 1)
    return remaining, bytes(value_bytes)


def read_compact_string(buffer: memoryview) -> BufferAnd[str]:
    remaining, bytes_value = read_compact_string_as_bytes(buffer)
    return remaining, bytes_value.decode()


def read_compact_string_nullable(buffer: memoryview) -> BufferAnd[str | None]:
    remaining, bytes_value = read_compact_string_as_bytes_nullable(buffer)
    if bytes_value is None:
        return remaining, None
    return remaining, bytes_value.decode()


def read_legacy_bytes(buffer: memoryview) -> BufferAnd[bytes]:
    remaining, length = read_int32(buffer)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where bytes was expected")
    remaining, bytes_view = read_exact(remaining, length)
    return remaining, bytes(bytes_view)


def read_nullable_legacy_bytes(buffer: memoryview) -> BufferAnd[bytes | None]:
    remaining, length = read_int32(buffer)
    if length == -1:
        return remaining, None
    remaining, bytes_view = read_exact(remaining, length)
    return remaining, bytes(bytes_view)


def read_legacy_string(buffer: memoryview) -> BufferAnd[str]:
    remaining, length = read_int16(buffer)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where string/bytes was expected")
    remaining, bytes_view = read_exact(remaining, length)
    return remaining, bytes(bytes_view).decode()


def read_nullable_legacy_string(buffer: memoryview) -> BufferAnd[str | None]:
    remaining, length = read_int16(buffer)
    if length == -1:
        return remaining, None
    remaining, bytes_view = read_exact(remaining, length)
    return remaining, bytes(bytes_view).decode()


read_legacy_array_length: Final = read_int32


def read_compact_array_length(buffer: memoryview) -> BufferAnd[int]:
    remaining, encoded_length = read_unsigned_varint(buffer)
    # Apache Kafka® uses the array size plus 1.
    return remaining, encoded_length - 1


def read_uuid(buffer: memoryview) -> BufferAnd[UUID | None]:
    remaining, bytes_view = read_exact(buffer, 16)
    if bytes_view == uuid_zero.bytes:
        return remaining, None
    return remaining, UUID(bytes=bytes(bytes_view))


P = TypeVar("P")
Q = TypeVar("Q")


def _materialize_and_return(
    generator: Generator[P, None, Q],
) -> tuple[Q, tuple[P, ...]]:
    values = []
    try:
        while True:
            values.append(next(generator))
    except StopIteration as stop:
        return stop.value, tuple(values)
    else:
        raise ValueError("Generator did not raise StopIteration")


def _read_length_items(
    item_reader: Reader[T],
    length: int,
    buffer: memoryview,
) -> Generator[T, None, memoryview]:
    remaining = buffer
    for _ in range(length):
        remaining, item_value = item_reader(remaining)
        yield item_value
    return remaining


def compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(buffer: memoryview) -> BufferAnd[tuple[T, ...] | None]:
        remaining, length = read_compact_array_length(buffer)
        if length == -1:
            return remaining, None
        return _materialize_and_return(
            _read_length_items(item_reader, length, remaining)
        )

    return read_compact_array


def legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(buffer: memoryview) -> BufferAnd[tuple[T, ...] | None]:
        remaining, length = read_legacy_array_length(buffer)
        if length == -1:
            return remaining, None
        return _materialize_and_return(
            _read_length_items(item_reader, length, remaining)
        )

    return read_compact_array


def read_error_code(buffer: memoryview) -> BufferAnd[ErrorCode]:
    remaining, error_code = read_int16(buffer)
    return remaining, ErrorCode(error_code)


def read_timedelta_i32(buffer: memoryview) -> BufferAnd[i32Timedelta]:
    remaining, milliseconds = read_int32(buffer)
    return remaining, datetime.timedelta(milliseconds=milliseconds)  # type: ignore[return-value]


def read_timedelta_i64(buffer: memoryview) -> BufferAnd[i64Timedelta]:
    remaining, milliseconds = read_int64(buffer)
    return remaining, datetime.timedelta(milliseconds=milliseconds)  # type: ignore[return-value]


def _tz_aware_from_i64(timestamp: i64) -> TZAware:
    dt = datetime.datetime.fromtimestamp(timestamp / 1000, datetime.UTC)
    try:
        return TZAware.truncate(dt)
    except TypeError as exception:
        raise OutOfBoundValue("Read invalid value for datetime") from exception


def read_datetime_i64(buffer: memoryview) -> BufferAnd[TZAware]:
    remaining, timestamp = read_int64(buffer)
    return remaining, _tz_aware_from_i64(timestamp)


def read_nullable_datetime_i64(buffer: memoryview) -> BufferAnd[TZAware | None]:
    remaining, timestamp = read_int64(buffer)
    if timestamp == -1:
        return remaining, None
    return remaining, _tz_aware_from_i64(timestamp)


try:
    import _kio_core
except ImportError:
    print("No compiled _kio_core found")
else:
    for name in _kio_core.__all__:
        globals()[name] = _kio_core.__dict__[name]


val = read_boolean(b"\x01123", 0)
assert val == (True, 1), val
val = read_boolean(b"\x00123", 0)
assert val == (False, 1), val

val = read_boolean(b"\x00\x01", 0)
assert val == (False, 1), val
val = read_boolean(b"\x00\x01", 1)
assert val == (True, 2), val
val = read_compact_string_as_bytes(b"\x04barfar", 0)
assert val == (b"bar", 4)

val = read_compact_string_as_bytes_nullable(b"\x04barfar", 0)
assert val == (b"bar", 4)

val = read_compact_string_as_bytes_nullable(b"\x00barfar", 0)
assert val == (None, 1), val

val = read_int8(b"\x01123", 0)
assert val == (1, 1), val
val = read_int8(b"\x00123", 0)
assert val == (0, 1), val

assert read_unsigned_varint(b"2", 0) == (50, 1)
val = read_unsigned_varint(b"u2Foo", 1)
assert val == (50, 2), val

val = read_compact_string( b"\x06hello", 0)
assert val == ("hello", 6), val

val = read_compact_string( b"xx\x06hello", 2)
assert val == ("hello", 8), val

value = "The quick brown 🦊 jumps over the lazy dog 🧖"
byte_value = value.encode()
byte_length = len(byte_value) + 1  # string length is offset by one
prefixed = b"xxx" + byte_length.to_bytes(1, "little") + byte_value
val = read_compact_string(prefixed + b"| cruft", 3)
assert val == (value, len(prefixed))

try: read_compact_string(b"doot\x20hello there \xf0\x9f\x91\x8b", 4)
except ValueError as exc: assert str(exc) == "Buffer is exhausted"
else: assert False

try: read_compact_string(b"\x00", 0)
except UnexpectedNull: pass
else: assert False

try: read_compact_string(b"cruft|\x00|cruft", 6)
except UnexpectedNull: pass
else: assert False

val = read_compact_string_nullable( b"xx\x06hello", 2)
assert val == ("hello", 8), val
assert read_compact_string_nullable(b"\x00", 0) == (None, 1)
assert read_compact_string_nullable(b"cruft|\x00|cruft", 6) == (None, 7)

print("ok")
raise SystemExit
