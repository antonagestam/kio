import asyncio
import io
import uuid

import pytest

from kio.schema.metadata.response.v5 import (
    MetadataResponseBroker as MetadataResponseBrokerV5,
)
from kio.schema.metadata.response.v12 import MetadataResponse
from kio.schema.metadata.response.v12 import (
    MetadataResponseBroker as MetadataResponseBrokerV12,
)
from kio.serial import decoders
from kio.serial.encoders import write_boolean
from kio.serial.encoders import write_compact_array_length
from kio.serial.encoders import write_compact_string
from kio.serial.encoders import write_empty_tagged_fields
from kio.serial.encoders import write_int16
from kio.serial.encoders import write_int32
from kio.serial.encoders import write_legacy_string
from kio.serial.encoders import write_nullable_compact_string
from kio.serial.encoders import write_uuid
from kio.serial.parse import get_decoder
from kio.serial.parse import parse_entity_async
from kio.serial.parse import parse_entity_sync


class TestGetDecoder:
    @pytest.mark.parametrize(
        "kafka_type, flexible, optional, expected",
        (
            ("int8", True, False, decoders.decode_int8),
            ("int8", False, False, decoders.decode_int8),
            ("int16", True, False, decoders.decode_int16),
            ("int16", False, False, decoders.decode_int16),
            ("int32", True, False, decoders.decode_int32),
            ("int32", False, False, decoders.decode_int32),
            ("int64", True, False, decoders.decode_int64),
            ("int64", False, False, decoders.decode_int64),
            ("uint8", True, False, decoders.decode_uint8),
            ("uint8", False, False, decoders.decode_uint8),
            ("uint16", True, False, decoders.decode_uint16),
            ("uint16", False, False, decoders.decode_uint16),
            ("uint32", True, False, decoders.decode_uint32),
            ("uint32", False, False, decoders.decode_uint32),
            ("uint64", True, False, decoders.decode_uint64),
            ("uint64", False, False, decoders.decode_uint64),
            ("string", True, False, decoders.decode_compact_string),
            ("string", True, True, decoders.decode_compact_string_nullable),
            ("string", False, False, decoders.decode_string),
            ("string", False, True, decoders.decode_string_nullable),
        ),
    )
    def test_can_match_kafka_type_with_decoder(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
        expected: decoders.Decoder,
    ) -> None:
        assert get_decoder(kafka_type, flexible, optional) == expected

    @pytest.mark.parametrize(
        "kafka_type, flexible, optional",
        (
            ("int32", True, True),
            ("int32", False, True),
        ),
    )
    def test_raises_not_implemented_error_for_invalid_combination(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
    ) -> None:
        with pytest.raises(NotImplementedError):
            get_decoder(kafka_type, flexible, optional)


def test_can_parse_entity(buffer: io.BytesIO) -> None:
    assert MetadataResponseBrokerV12.__flexible__
    # node_id
    write_int32(buffer, 123)
    # host
    write_compact_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, 23_126)
    # rack
    write_compact_string(buffer, "da best")
    # tagged fields
    write_empty_tagged_fields(buffer)

    buffer.seek(0)
    instance = parse_entity_sync(buffer, MetadataResponseBrokerV12)
    assert isinstance(instance, MetadataResponseBrokerV12)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"


def test_can_parse_legacy_entity(buffer: io.BytesIO) -> None:
    assert not MetadataResponseBrokerV5.__flexible__
    # node_id
    write_int32(buffer, 123)
    # host
    write_legacy_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, 23_126)
    # rack
    write_legacy_string(buffer, "da best")
    # tagged fields
    write_empty_tagged_fields(buffer)

    buffer.seek(0)
    instance = parse_entity_sync(buffer, MetadataResponseBrokerV5)
    assert isinstance(instance, MetadataResponseBrokerV5)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"


def test_can_parse_complex_entity(buffer: io.BytesIO) -> None:
    assert MetadataResponse.__flexible__

    # throttle time
    write_int32(buffer, 123)

    # brokers
    write_compact_array_length(buffer, 2)
    for i in range(1, 3):
        # node_id
        write_int32(buffer, i)
        # host
        write_compact_string(buffer, "kafka.aiven.test")
        # port
        write_int32(buffer, i**i)
        # rack
        write_compact_string(buffer, "da best")

        write_empty_tagged_fields(buffer)

    # cluster_id
    write_nullable_compact_string(buffer, None)

    # controller id
    write_int32(buffer, 321)

    # topics
    write_compact_array_length(buffer, 1)
    topic_id = uuid.uuid4()
    for i in range(1):
        # error code
        write_int16(buffer, 0)
        # name
        write_compact_string(buffer, f"great topic {i}")
        # topic_id
        write_uuid(buffer, topic_id)
        # is_internal
        write_boolean(buffer, False)

        # partitions
        write_compact_array_length(buffer, 1)
        for ii in range(1):
            # error_code
            write_int16(buffer, 0)
            # partition_index
            write_int32(buffer, ii)
            # leader_id
            write_int32(buffer, 321)
            # leader_epoch
            write_int32(buffer, 13)
            # replica_nodes
            write_compact_array_length(buffer, 0)
            # isr_nodes
            write_compact_array_length(buffer, 0)
            # offline_replicas
            write_compact_array_length(buffer, 3)
            write_int32(buffer, 123)
            write_int32(buffer, 1090)
            write_int32(buffer, 3321)
            # tagged fields
            write_empty_tagged_fields(buffer)

        # topic_authorized_operations
        write_int32(buffer, 0)
        # tagged fields
        write_empty_tagged_fields(buffer)

    # main entity tagged fields
    write_empty_tagged_fields(buffer)

    buffer.seek(0)

    instance = parse_entity_sync(buffer, MetadataResponse)
    assert isinstance(instance, MetadataResponse)

    assert instance.throttle_time_ms == 123
    assert len(instance.brokers) == 2
    assert instance.cluster_id is None
    assert instance.controller_id == 321
    assert len(instance.topics) == 1
    assert instance.topics[0].error_code == 0
    assert instance.topics[0].name == "great topic 0"
    assert instance.topics[0].topic_id == topic_id
    assert instance.topics[0].is_internal is False
    assert len(instance.topics[0].partitions) == 1
    assert instance.topics[0].topic_authorized_operations == 0


async def test_can_parse_complex_entity_async(
    stream_writer: asyncio.StreamWriter,
    stream_reader: asyncio.StreamReader,
) -> None:
    assert MetadataResponse.__flexible__

    # throttle time
    write_int32(stream_writer, 123)

    # brokers
    write_compact_array_length(stream_writer, 2)
    for i in range(1, 3):
        # node_id
        write_int32(stream_writer, i)
        # host
        write_compact_string(stream_writer, "kafka.aiven.test")
        # port
        write_int32(stream_writer, i**i)
        # rack
        write_compact_string(stream_writer, "da best")

        write_empty_tagged_fields(stream_writer)

    # cluster_id
    write_nullable_compact_string(stream_writer, None)

    # controller id
    write_int32(stream_writer, 321)

    # topics
    write_compact_array_length(stream_writer, 1)
    topic_id = uuid.uuid4()
    for i in range(1):
        # error code
        write_int16(stream_writer, 0)
        # name
        write_compact_string(stream_writer, f"great topic {i}")
        # topic_id
        write_uuid(stream_writer, topic_id)
        # is_internal
        write_boolean(stream_writer, False)

        # partitions
        write_compact_array_length(stream_writer, 1)
        for ii in range(1):
            # error_code
            write_int16(stream_writer, 0)
            # partition_index
            write_int32(stream_writer, ii)
            # leader_id
            write_int32(stream_writer, 321)
            # leader_epoch
            write_int32(stream_writer, 13)
            # replica_nodes
            write_compact_array_length(stream_writer, 0)
            # isr_nodes
            write_compact_array_length(stream_writer, 0)
            # offline_replicas
            write_compact_array_length(stream_writer, 3)
            write_int32(stream_writer, 123)
            write_int32(stream_writer, 1090)
            write_int32(stream_writer, 3321)
            # tagged fields
            write_empty_tagged_fields(stream_writer)

        # topic_authorized_operations
        write_int32(stream_writer, 0)
        # tagged fields
        write_empty_tagged_fields(stream_writer)

    # main entity tagged fields
    write_empty_tagged_fields(stream_writer)

    await stream_writer.drain()

    instance = await parse_entity_async(stream_reader, MetadataResponse)
    assert isinstance(instance, MetadataResponse)

    assert instance.throttle_time_ms == 123
    assert len(instance.brokers) == 2
    assert instance.cluster_id is None
    assert instance.controller_id == 321
    assert len(instance.topics) == 1
    assert instance.topics[0].error_code == 0
    assert instance.topics[0].name == "great topic 0"
    assert instance.topics[0].topic_id == topic_id
    assert instance.topics[0].is_internal is False
    assert len(instance.topics[0].partitions) == 1
    assert instance.topics[0].topic_authorized_operations == 0