"""
Generated from DescribeUserScramCredentialsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v1.header import ResponseHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class CredentialInfo:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    mechanism: i8 = field(metadata={"kafka_type": "int8"})
    """The SCRAM mechanism."""
    iterations: i32 = field(metadata={"kafka_type": "int32"})
    """The number of iterations used in the SCRAM credential."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    user: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The user-level error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The user-level error message, if any."""
    credential_infos: tuple[CredentialInfo, ...]
    """The mechanism and related information associated with the user's SCRAM credentials."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The message-level error code, 0 except for user authorization or infrastructure issues."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The message-level error message, if any."""
    results: tuple[DescribeUserScramCredentialsResult, ...]
    """The results for descriptions, one per user."""
