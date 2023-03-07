"""
Generated from FindCoordinatorResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class Coordinator:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(10)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    key: str = field(metadata={"kafka_type": "string"})
    """The coordinator key."""
    node_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The node id."""
    host: str = field(metadata={"kafka_type": "string"})
    """The host name."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The port."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorResponse:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(10)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    coordinators: tuple[Coordinator, ...]
    """Each coordinator result in the response"""
