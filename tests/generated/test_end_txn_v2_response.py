from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.end_txn.v2.response import EndTxnResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_end_txn_response: Final = entity_reader(EndTxnResponse)


@pytest.mark.roundtrip
@given(from_type(EndTxnResponse))
def test_end_txn_response_roundtrip(instance: EndTxnResponse) -> None:
    writer = entity_writer(EndTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_end_txn_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(EndTxnResponse))
def test_end_txn_response_java(
    instance: EndTxnResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
