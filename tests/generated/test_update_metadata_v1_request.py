from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_metadata.v1.request import UpdateMetadataBroker
from kio.schema.update_metadata.v1.request import UpdateMetadataEndpoint
from kio.schema.update_metadata.v1.request import UpdateMetadataPartitionState
from kio.schema.update_metadata.v1.request import UpdateMetadataRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_update_metadata_partition_state: Final = entity_reader(
    UpdateMetadataPartitionState
)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataPartitionState))
@settings(max_examples=1)
def test_update_metadata_partition_state_roundtrip(
    instance: UpdateMetadataPartitionState,
) -> None:
    writer = entity_writer(UpdateMetadataPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_metadata_partition_state(buffer)
    assert instance == result


read_update_metadata_endpoint: Final = entity_reader(UpdateMetadataEndpoint)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataEndpoint))
@settings(max_examples=1)
def test_update_metadata_endpoint_roundtrip(instance: UpdateMetadataEndpoint) -> None:
    writer = entity_writer(UpdateMetadataEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_metadata_endpoint(buffer)
    assert instance == result


read_update_metadata_broker: Final = entity_reader(UpdateMetadataBroker)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataBroker))
@settings(max_examples=1)
def test_update_metadata_broker_roundtrip(instance: UpdateMetadataBroker) -> None:
    writer = entity_writer(UpdateMetadataBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_metadata_broker(buffer)
    assert instance == result


read_update_metadata_request: Final = entity_reader(UpdateMetadataRequest)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataRequest))
@settings(max_examples=1)
def test_update_metadata_request_roundtrip(instance: UpdateMetadataRequest) -> None:
    writer = entity_writer(UpdateMetadataRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_metadata_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateMetadataRequest))
def test_update_metadata_request_java(
    instance: UpdateMetadataRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
