"""
Generated from MetadataRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/MetadataRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequestTopic:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[MetadataRequestTopic, ...]
    """The topics to fetch metadata for."""
