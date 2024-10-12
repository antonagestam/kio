from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.end_quorum_epoch.v0.request import EndQuorumEpochRequest
from kio.schema.end_quorum_epoch.v0.request import PartitionData
from kio.schema.end_quorum_epoch.v0.request import TopicData
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


read_end_quorum_epoch_request: Final = entity_reader(EndQuorumEpochRequest)


@pytest.mark.roundtrip
@given(from_type(EndQuorumEpochRequest))
def test_end_quorum_epoch_request_roundtrip(instance: EndQuorumEpochRequest) -> None:
    writer = entity_writer(EndQuorumEpochRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_end_quorum_epoch_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(EndQuorumEpochRequest))
def test_end_quorum_epoch_request_java(
    instance: EndQuorumEpochRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
