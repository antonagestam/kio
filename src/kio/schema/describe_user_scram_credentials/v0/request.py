"""
Generated from DescribeUserScramCredentialsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.request_header.v2.header import RequestHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class UserName:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The user name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeUserScramCredentialsRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(50)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    users: tuple[UserName, ...]
    """The users to describe, or null/empty to describe all users."""
