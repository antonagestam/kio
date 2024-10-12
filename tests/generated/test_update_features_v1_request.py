from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_features.v1.request import FeatureUpdateKey
from kio.schema.update_features.v1.request import UpdateFeaturesRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_feature_update_key: Final = entity_reader(FeatureUpdateKey)


@pytest.mark.roundtrip
@given(from_type(FeatureUpdateKey))
def test_feature_update_key_roundtrip(instance: FeatureUpdateKey) -> None:
    writer = entity_writer(FeatureUpdateKey)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_feature_update_key(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


read_update_features_request: Final = entity_reader(UpdateFeaturesRequest)


@pytest.mark.roundtrip
@given(from_type(UpdateFeaturesRequest))
def test_update_features_request_roundtrip(instance: UpdateFeaturesRequest) -> None:
    writer = entity_writer(UpdateFeaturesRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        remaining, result = read_update_features_request(
            buffer.getbuffer(),
        )

    assert remaining == b""
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateFeaturesRequest))
def test_update_features_request_java(
    instance: UpdateFeaturesRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
