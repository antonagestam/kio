from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_delete.v0.response import OffsetDeleteResponse
from kio.schema.offset_delete.v0.response import OffsetDeleteResponsePartition
from kio.schema.offset_delete.v0.response import OffsetDeleteResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_delete_response_partition: Final = entity_reader(
    OffsetDeleteResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteResponsePartition))
def test_offset_delete_response_partition_roundtrip(
    instance: OffsetDeleteResponsePartition,
) -> None:
    writer = entity_writer(OffsetDeleteResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_offset_delete_response_partition(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_offset_delete_response_topic: Final = entity_reader(OffsetDeleteResponseTopic)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteResponseTopic))
def test_offset_delete_response_topic_roundtrip(
    instance: OffsetDeleteResponseTopic,
) -> None:
    writer = entity_writer(OffsetDeleteResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_offset_delete_response_topic(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_offset_delete_response: Final = entity_reader(OffsetDeleteResponse)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteResponse))
def test_offset_delete_response_roundtrip(instance: OffsetDeleteResponse) -> None:
    writer = entity_writer(OffsetDeleteResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_offset_delete_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(OffsetDeleteResponse))
def test_offset_delete_response_java(
    instance: OffsetDeleteResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
