from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.alter_partition.v3.request import AlterPartitionRequest
from kio.schema.alter_partition.v3.request import BrokerState
from kio.schema.alter_partition.v3.request import PartitionData
from kio.schema.alter_partition.v3.request import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_broker_state: Final = entity_reader(BrokerState)


@pytest.mark.roundtrip
@given(from_type(BrokerState))
def test_broker_state_roundtrip(instance: BrokerState) -> None:
    writer = entity_writer(BrokerState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_broker_state(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


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


read_topic_data: Final = entity_reader(TopicData)


@pytest.mark.roundtrip
@given(from_type(TopicData))
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_topic_data(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_alter_partition_request: Final = entity_reader(AlterPartitionRequest)


@pytest.mark.roundtrip
@given(from_type(AlterPartitionRequest))
def test_alter_partition_request_roundtrip(instance: AlterPartitionRequest) -> None:
    writer = entity_writer(AlterPartitionRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_alter_partition_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterPartitionRequest))
def test_alter_partition_request_java(
    instance: AlterPartitionRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
