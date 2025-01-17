from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v4.response import DescribeLogDirsPartition
from kio.schema.describe_log_dirs.v4.response import DescribeLogDirsResponse
from kio.schema.describe_log_dirs.v4.response import DescribeLogDirsResult
from kio.schema.describe_log_dirs.v4.response import DescribeLogDirsTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_log_dirs_partition: Final = entity_reader(DescribeLogDirsPartition)


@pytest.mark.roundtrip
@given(from_type(DescribeLogDirsPartition))
@settings(max_examples=1)
def test_describe_log_dirs_partition_roundtrip(
    instance: DescribeLogDirsPartition,
) -> None:
    writer = entity_writer(DescribeLogDirsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_partition(buffer)
    assert instance == result


read_describe_log_dirs_topic: Final = entity_reader(DescribeLogDirsTopic)


@pytest.mark.roundtrip
@given(from_type(DescribeLogDirsTopic))
@settings(max_examples=1)
def test_describe_log_dirs_topic_roundtrip(instance: DescribeLogDirsTopic) -> None:
    writer = entity_writer(DescribeLogDirsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_topic(buffer)
    assert instance == result


read_describe_log_dirs_result: Final = entity_reader(DescribeLogDirsResult)


@pytest.mark.roundtrip
@given(from_type(DescribeLogDirsResult))
@settings(max_examples=1)
def test_describe_log_dirs_result_roundtrip(instance: DescribeLogDirsResult) -> None:
    writer = entity_writer(DescribeLogDirsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_result(buffer)
    assert instance == result


read_describe_log_dirs_response: Final = entity_reader(DescribeLogDirsResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeLogDirsResponse))
@settings(max_examples=1)
def test_describe_log_dirs_response_roundtrip(
    instance: DescribeLogDirsResponse,
) -> None:
    writer = entity_writer(DescribeLogDirsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeLogDirsResponse))
def test_describe_log_dirs_response_java(
    instance: DescribeLogDirsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
