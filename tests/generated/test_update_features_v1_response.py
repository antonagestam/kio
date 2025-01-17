from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_features.v1.response import UpdatableFeatureResult
from kio.schema.update_features.v1.response import UpdateFeaturesResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_updatable_feature_result: Final = entity_reader(UpdatableFeatureResult)


@pytest.mark.roundtrip
@given(from_type(UpdatableFeatureResult))
@settings(max_examples=1)
def test_updatable_feature_result_roundtrip(instance: UpdatableFeatureResult) -> None:
    writer = entity_writer(UpdatableFeatureResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_updatable_feature_result(buffer)
    assert instance == result


read_update_features_response: Final = entity_reader(UpdateFeaturesResponse)


@pytest.mark.roundtrip
@given(from_type(UpdateFeaturesResponse))
@settings(max_examples=1)
def test_update_features_response_roundtrip(instance: UpdateFeaturesResponse) -> None:
    writer = entity_writer(UpdateFeaturesResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_features_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateFeaturesResponse))
def test_update_features_response_java(
    instance: UpdateFeaturesResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
