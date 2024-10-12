from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_metadata.v0.response import UpdateMetadataResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_update_metadata_response: Final = entity_reader(UpdateMetadataResponse)


@pytest.mark.roundtrip
@given(from_type(UpdateMetadataResponse))
def test_update_metadata_response_roundtrip(instance: UpdateMetadataResponse) -> None:
    writer = entity_writer(UpdateMetadataResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_update_metadata_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateMetadataResponse))
def test_update_metadata_response_java(
    instance: UpdateMetadataResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
