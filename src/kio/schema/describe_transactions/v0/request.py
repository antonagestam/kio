"""
Generated from DescribeTransactionsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTransactionsRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(65)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_ids: tuple[TransactionalId, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Array of transactionalIds to include in describe results. If empty, then no results will be returned."""
