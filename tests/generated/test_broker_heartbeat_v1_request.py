from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.broker_heartbeat.v1.request import BrokerHeartbeatRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_broker_heartbeat_request: Final = entity_reader(BrokerHeartbeatRequest)


@pytest.mark.roundtrip
@given(from_type(BrokerHeartbeatRequest))
def test_broker_heartbeat_request_roundtrip(instance: BrokerHeartbeatRequest) -> None:
    writer = entity_writer(BrokerHeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_broker_heartbeat_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(BrokerHeartbeatRequest))
def test_broker_heartbeat_request_java(
    instance: BrokerHeartbeatRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
