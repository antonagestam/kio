from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.unregister_broker.v0.response import UnregisterBrokerResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_unregister_broker_response: Final = entity_reader(UnregisterBrokerResponse)


@pytest.mark.roundtrip
@given(from_type(UnregisterBrokerResponse))
def test_unregister_broker_response_roundtrip(
    instance: UnregisterBrokerResponse,
) -> None:
    writer = entity_writer(UnregisterBrokerResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_unregister_broker_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UnregisterBrokerResponse))
def test_unregister_broker_response_java(
    instance: UnregisterBrokerResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
