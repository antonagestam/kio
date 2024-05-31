"""
Generated from ``clients/src/main/resources/common/message/AlterUserScramCredentialsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, if any."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[AlterUserScramCredentialsResult, ...]
    """The results for deletions and alterations, one per affected user."""
