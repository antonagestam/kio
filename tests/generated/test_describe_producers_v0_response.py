from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_producers.v0.response import DescribeProducersResponse
from kio.schema.describe_producers.v0.response import PartitionResponse
from kio.schema.describe_producers.v0.response import ProducerState
from kio.schema.describe_producers.v0.response import TopicResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_producer_state: Final = entity_reader(ProducerState)


@pytest.mark.roundtrip
@given(from_type(ProducerState))
def test_producer_state_roundtrip(instance: ProducerState) -> None:
    writer = entity_writer(ProducerState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_producer_state(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_partition_response: Final = entity_reader(PartitionResponse)


@pytest.mark.roundtrip
@given(from_type(PartitionResponse))
def test_partition_response_roundtrip(instance: PartitionResponse) -> None:
    writer = entity_writer(PartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_partition_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_topic_response: Final = entity_reader(TopicResponse)


@pytest.mark.roundtrip
@given(from_type(TopicResponse))
def test_topic_response_roundtrip(instance: TopicResponse) -> None:
    writer = entity_writer(TopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_topic_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_describe_producers_response: Final = entity_reader(DescribeProducersResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeProducersResponse))
def test_describe_producers_response_roundtrip(
    instance: DescribeProducersResponse,
) -> None:
    writer = entity_writer(DescribeProducersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_describe_producers_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeProducersResponse))
def test_describe_producers_response_java(
    instance: DescribeProducersResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
