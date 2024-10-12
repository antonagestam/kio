from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.request_header.v0.header import RequestHeader
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_request_header: Final = entity_reader(RequestHeader)


@pytest.mark.roundtrip
@given(from_type(RequestHeader))
def test_request_header_roundtrip(instance: RequestHeader) -> None:
    writer = entity_writer(RequestHeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_request_header(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(RequestHeader))
def test_request_header_java(instance: RequestHeader, java_tester: JavaTester) -> None:
    java_tester.test(instance)
