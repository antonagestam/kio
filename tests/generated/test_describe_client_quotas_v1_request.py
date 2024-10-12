from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_client_quotas.v1.request import ComponentData
from kio.schema.describe_client_quotas.v1.request import DescribeClientQuotasRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_component_data: Final = entity_reader(ComponentData)


@pytest.mark.roundtrip
@given(from_type(ComponentData))
def test_component_data_roundtrip(instance: ComponentData) -> None:
    writer = entity_writer(ComponentData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_component_data(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_describe_client_quotas_request: Final = entity_reader(DescribeClientQuotasRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeClientQuotasRequest))
def test_describe_client_quotas_request_roundtrip(
    instance: DescribeClientQuotasRequest,
) -> None:
    writer = entity_writer(DescribeClientQuotasRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_describe_client_quotas_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeClientQuotasRequest))
def test_describe_client_quotas_request_java(
    instance: DescribeClientQuotasRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
