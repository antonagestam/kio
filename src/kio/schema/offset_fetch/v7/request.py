"""
Generated from OffsetFetchRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequestTopic:
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partition indexes we would like to fetch offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequest:
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group to fetch offsets for."""
    topics: tuple[OffsetFetchRequestTopic, ...]
    """Each topic we would like to fetch offsets for, or null to fetch offsets for all topics."""
    require_stable: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Whether broker should hold on returning unstable offsets but set a retriable error code for the partitions."""
