import io
import uuid
from ast import parse

from typing import TypeVar

import pytest

from hypothesis import given
from hypothesis.strategies import binary
from hypothesis.strategies import booleans
from hypothesis.strategies import from_type
from hypothesis.strategies import integers
from hypothesis.strategies import none
from hypothesis.strategies import text
from hypothesis.strategies import uuids

from kio.schema.metadata.v12.response import MetadataResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.readers import Reader
from kio.serial.readers import read_boolean
from kio.serial.readers import read_compact_array_length
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_compact_string_as_bytes
from kio.serial.readers import read_compact_string_as_bytes_nullable
from kio.serial.readers import read_compact_string_nullable
from kio.serial.readers import read_int8
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_int64
from kio.serial.readers import read_legacy_array_length
from kio.serial.readers import read_legacy_bytes
from kio.serial.readers import read_legacy_string
from kio.serial.readers import read_nullable_legacy_string
from kio.serial.readers import read_uint8
from kio.serial.readers import read_uint16
from kio.serial.readers import read_uint32
from kio.serial.readers import read_uint64
from kio.serial.readers import read_unsigned_varint
from kio.serial.readers import read_uuid
from kio.serial.writers import Writer
from kio.serial.writers import write_boolean
from kio.serial.writers import write_compact_array_length
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_int64
from kio.serial.writers import write_legacy_array_length
from kio.serial.writers import write_legacy_bytes
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_nullable_compact_string
from kio.serial.writers import write_nullable_legacy_string
from kio.serial.writers import write_uint8
from kio.serial.writers import write_uint16
from kio.serial.writers import write_uint32
from kio.serial.writers import write_uint64
from kio.serial.writers import write_unsigned_varint
from kio.serial.writers import write_uuid
from tests.read_exhausted import exhausted

pytestmark = pytest.mark.roundtrip


@given(booleans(), booleans())
def test_booleans_roundtrip_sync(a: bool, b: bool) -> None:
    buffer = io.BytesIO()
    write_boolean(buffer, a)
    write_boolean(buffer, b)

    remaining, parsed_a = read_boolean(buffer.getbuffer())
    assert parsed_a is a
    parsed_b = exhausted(read_boolean(remaining))
    assert parsed_b is b


_I = TypeVar("_I", bound=int, contravariant=True)


def create_integer_roundtrip_test(
    int_writer: Writer[_I],
    int_reader: Reader[int],
    min_value: int,
    max_value: int,
) -> type:
    parameterize = given(
        integers(min_value=min_value, max_value=max_value),
        integers(min_value=min_value, max_value=max_value),
    )

    class Test:
        @parameterize
        def test_roundtrip(self, a: _I, b: _I) -> None:
            buffer = io.BytesIO()
            int_writer(buffer, a)
            int_writer(buffer, b)

            remaining, parsed_a = int_reader(buffer.getbuffer())
            assert parsed_a == a
            parsed_b = exhausted(int_reader(remaining))
            assert parsed_b == b

    return Test


TestInt8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int8,
    int_reader=read_int8,
    min_value=-(2**7),
    max_value=2**7 - 1,
)
TestInt16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int16,
    int_reader=read_int16,
    min_value=-(2**15),
    max_value=2**15 - 1,
)
TestInt32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int32,
    int_reader=read_int32,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestInt64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int64,
    int_reader=read_int64,
    min_value=-(2**63),
    max_value=2**63 - 1,
)
TestUint8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint8,
    int_reader=read_uint8,
    min_value=0,
    max_value=2**7 - 1,
)
TestUint16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint16,
    int_reader=read_uint16,
    min_value=0,
    max_value=2**15 - 1,
)
TestUint32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint32,
    int_reader=read_uint32,
    min_value=0,
    max_value=2**31 - 1,
)
TestUint64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint64,
    int_reader=read_uint64,
    min_value=0,
    max_value=2**63 - 1,
)
TestUnsignedVarintRoundtrip = create_integer_roundtrip_test(
    int_writer=write_unsigned_varint,
    int_reader=read_unsigned_varint,
    min_value=0,
    max_value=2**31 - 1,
)
TestLegacyArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_legacy_array_length,
    int_reader=read_legacy_array_length,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestCompactArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_compact_array_length,
    int_reader=read_compact_array_length,
    min_value=-1,
    max_value=2**31 - 2,
)


@given(text(), text())
def test_compact_string_roundtrip_sync(a: str, b: str) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)

    remaining, parsed_a = read_compact_string(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_compact_string(remaining))
    assert parsed_b == b


@given(binary(), binary())
def test_compact_bytes_roundtrip(a: bytes, b: bytes) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)

    remaining, parsed_a = read_compact_string_as_bytes(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_compact_string_as_bytes(remaining))
    assert parsed_b == b


def test_compact_bytes_roundtrip_none() -> None:
    buffer = io.BytesIO()
    write_nullable_compact_string(buffer, None)
    write_nullable_compact_string(buffer, None)

    remaining, value = read_compact_string_as_bytes_nullable(buffer.getbuffer())
    assert value is None
    value = exhausted(read_compact_string_as_bytes_nullable(remaining))
    assert value is None


def test_compact_string_roundtrip_none() -> None:
    buffer = io.BytesIO()
    write_nullable_compact_string(buffer, None)
    write_nullable_compact_string(buffer, None)

    remaining, value = read_compact_string_nullable(buffer.getbuffer())
    assert value is None
    value = exhausted(read_compact_string_nullable(remaining))
    assert value is None


@given(text(), text())
def test_legacy_string_roundtrip(a: str, b: str) -> None:
    buffer = io.BytesIO()
    write_legacy_string(buffer, a)
    write_legacy_string(buffer, b)

    remaining, parsed_a = read_legacy_string(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_legacy_string(buffer.getbuffer()))
    assert parsed_b == b


@given(text() | none(), text() | none())
def test_nullable_legacy_string_roundtrip(a: str | None, b: str | None) -> None:
    buffer = io.BytesIO()
    write_nullable_legacy_string(buffer, a)
    write_nullable_legacy_string(buffer, b)

    remaining, parsed_a = read_nullable_legacy_string(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_nullable_legacy_string(remaining))
    assert parsed_b == b


@given(binary(), binary())
def test_legacy_bytes_roundtrip(a: bytes, b: bytes) -> None:
    buffer = io.BytesIO()
    write_legacy_bytes(buffer, a)
    write_legacy_bytes(buffer, b)

    remaining, parsed_a = read_legacy_bytes(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_legacy_bytes(remaining))
    assert parsed_b == b


@given(uuids() | none(), uuids() | none())
def test_uuid_roundtrip(a: uuid.UUID | None, b: uuid.UUID | None) -> None:
    buffer = io.BytesIO()
    write_uuid(buffer, a)
    write_uuid(buffer, b)

    remaining, parsed_a = read_uuid(buffer.getbuffer())
    assert parsed_a == a
    parsed_b = exhausted(read_uuid(remaining))
    assert parsed_b == b


@given(from_type(MetadataResponse))
async def test_flexible_entity_roundtrip(instance: MetadataResponse) -> None:
    buffer = io.BytesIO()
    write_metadata_response = entity_writer(MetadataResponse)
    write_metadata_response(buffer, instance)

    result = exhausted(entity_reader(MetadataResponse)(buffer.getbuffer()))
    assert result == instance
