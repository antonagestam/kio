from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_metadata.v0.request import UpdateMetadataBroker
from kio.schema.update_metadata.v0.request import UpdateMetadataPartitionState
from kio.schema.update_metadata.v0.request import UpdateMetadataRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_update_metadata_partition_state: Final = entity_reader(
    UpdateMetadataPartitionState
)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataPartitionState))
def test_update_metadata_partition_state_roundtrip(
    instance: UpdateMetadataPartitionState,
) -> None:
    writer = entity_writer(UpdateMetadataPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_update_metadata_partition_state(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_update_metadata_broker: Final = entity_reader(UpdateMetadataBroker)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataBroker))
def test_update_metadata_broker_roundtrip(instance: UpdateMetadataBroker) -> None:
    writer = entity_writer(UpdateMetadataBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_update_metadata_broker(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_update_metadata_request: Final = entity_reader(UpdateMetadataRequest)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataRequest))
def test_update_metadata_request_roundtrip(instance: UpdateMetadataRequest) -> None:
    writer = entity_writer(UpdateMetadataRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_update_metadata_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateMetadataRequest))
def test_update_metadata_request_java(
    instance: UpdateMetadataRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
