from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.fetch.v3.response import FetchableTopicResponse
from kio.schema.fetch.v3.response import FetchResponse
from kio.schema.fetch.v3.response import PartitionData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_partition_data(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_fetchable_topic_response: Final = entity_reader(FetchableTopicResponse)


@pytest.mark.roundtrip
@given(from_type(FetchableTopicResponse))
def test_fetchable_topic_response_roundtrip(instance: FetchableTopicResponse) -> None:
    writer = entity_writer(FetchableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_fetchable_topic_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_fetch_response: Final = entity_reader(FetchResponse)


@pytest.mark.roundtrip
@given(from_type(FetchResponse))
def test_fetch_response_roundtrip(instance: FetchResponse) -> None:
    writer = entity_writer(FetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_fetch_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(FetchResponse))
def test_fetch_response_java(instance: FetchResponse, java_tester: JavaTester) -> None:
    java_tester.test(instance)
