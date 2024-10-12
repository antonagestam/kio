from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_records.v1.response import DeleteRecordsPartitionResult
from kio.schema.delete_records.v1.response import DeleteRecordsResponse
from kio.schema.delete_records.v1.response import DeleteRecordsTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_records_partition_result: Final = entity_reader(
    DeleteRecordsPartitionResult
)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsPartitionResult))
def test_delete_records_partition_result_roundtrip(
    instance: DeleteRecordsPartitionResult,
) -> None:
    writer = entity_writer(DeleteRecordsPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_delete_records_partition_result(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_delete_records_topic_result: Final = entity_reader(DeleteRecordsTopicResult)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsTopicResult))
def test_delete_records_topic_result_roundtrip(
    instance: DeleteRecordsTopicResult,
) -> None:
    writer = entity_writer(DeleteRecordsTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_delete_records_topic_result(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_delete_records_response: Final = entity_reader(DeleteRecordsResponse)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsResponse))
def test_delete_records_response_roundtrip(instance: DeleteRecordsResponse) -> None:
    writer = entity_writer(DeleteRecordsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_delete_records_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteRecordsResponse))
def test_delete_records_response_java(
    instance: DeleteRecordsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
