"""
Generated from ``clients/src/main/resources/common/message/ListGroupsRequest.json``.
"""

from dataclasses import dataclass
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
