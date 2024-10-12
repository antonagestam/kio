from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v1.request import DescribableLogDirTopic
from kio.schema.describe_log_dirs.v1.request import DescribeLogDirsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describable_log_dir_topic: Final = entity_reader(DescribableLogDirTopic)


@pytest.mark.roundtrip
@given(from_type(DescribableLogDirTopic))
def test_describable_log_dir_topic_roundtrip(instance: DescribableLogDirTopic) -> None:
    writer = entity_writer(DescribableLogDirTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_describable_log_dir_topic(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_describe_log_dirs_request: Final = entity_reader(DescribeLogDirsRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeLogDirsRequest))
def test_describe_log_dirs_request_roundtrip(instance: DescribeLogDirsRequest) -> None:
    writer = entity_writer(DescribeLogDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_describe_log_dirs_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeLogDirsRequest))
def test_describe_log_dirs_request_java(
    instance: DescribeLogDirsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
