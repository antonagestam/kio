"""
Generated from AlterUserScramCredentialsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterUserScramCredentialsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ScramCredentialDeletion:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    mechanism: i8 = field(metadata={"kafka_type": "int8"})
    """The SCRAM mechanism."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ScramCredentialUpsertion:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The user name."""
    mechanism: i8 = field(metadata={"kafka_type": "int8"})
    """The SCRAM mechanism."""
    iterations: i32 = field(metadata={"kafka_type": "int32"})
    """The number of iterations."""
    salt: bytes = field(metadata={"kafka_type": "bytes"})
    """A random salt generated by the client."""
    salted_password: bytes = field(metadata={"kafka_type": "bytes"})
    """The salted password."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterUserScramCredentialsRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(51)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    deletions: tuple[ScramCredentialDeletion, ...]
    """The SCRAM credentials to remove."""
    upsertions: tuple[ScramCredentialUpsertion, ...]
    """The SCRAM credentials to update/insert."""
