from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.sync_group.v3.response import SyncGroupResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sync_group_response: Final = entity_reader(SyncGroupResponse)


@pytest.mark.roundtrip
@given(from_type(SyncGroupResponse))
def test_sync_group_response_roundtrip(instance: SyncGroupResponse) -> None:
    writer = entity_writer(SyncGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_sync_group_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SyncGroupResponse))
def test_sync_group_response_java(
    instance: SyncGroupResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
