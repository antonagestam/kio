"""
Generated from AllocateProducerIdsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i64
from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class AllocateProducerIdsRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(67)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The epoch of the requesting broker"""
