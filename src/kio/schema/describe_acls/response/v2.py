"""
Generated from DescribeAclsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class AclDescription:
    __flexible__: ClassVar[bool] = True
    principal: str = field(metadata={"kafka_type": "string"})
    """The ACL principal."""
    host: str = field(metadata={"kafka_type": "string"})
    """The ACL host."""
    operation: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL operation."""
    permission_type: i8 = field(metadata={"kafka_type": "int8"})
    """The ACL permission type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResource:
    __flexible__: ClassVar[bool] = True
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    pattern_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(3))
    """The resource pattern type."""
    acls: tuple[AclDescription, ...]
    """The ACLs."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeAclsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    resources: tuple[DescribeAclsResource, ...]
    """Each Resource that is referenced in an ACL."""
