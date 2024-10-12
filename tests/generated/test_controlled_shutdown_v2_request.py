from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.controlled_shutdown.v2.request import ControlledShutdownRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_controlled_shutdown_request: Final = entity_reader(ControlledShutdownRequest)


@pytest.mark.roundtrip
@given(from_type(ControlledShutdownRequest))
def test_controlled_shutdown_request_roundtrip(
    instance: ControlledShutdownRequest,
) -> None:
    writer = entity_writer(ControlledShutdownRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_controlled_shutdown_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ControlledShutdownRequest))
def test_controlled_shutdown_request_java(
    instance: ControlledShutdownRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
