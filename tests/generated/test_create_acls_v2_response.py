from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.create_acls.v2.response import AclCreationResult
from kio.schema.create_acls.v2.response import CreateAclsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_acl_creation_result: Final = entity_reader(AclCreationResult)


@pytest.mark.roundtrip
@given(from_type(AclCreationResult))
def test_acl_creation_result_roundtrip(instance: AclCreationResult) -> None:
    writer = entity_writer(AclCreationResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_acl_creation_result(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_create_acls_response: Final = entity_reader(CreateAclsResponse)


@pytest.mark.roundtrip
@given(from_type(CreateAclsResponse))
def test_create_acls_response_roundtrip(instance: CreateAclsResponse) -> None:
    writer = entity_writer(CreateAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_create_acls_response(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(CreateAclsResponse))
def test_create_acls_response_java(
    instance: CreateAclsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
