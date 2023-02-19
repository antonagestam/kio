"""
Generated from DescribeQuorumResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaState:
    __flexible__: ClassVar[bool] = True
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    log_end_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last known log end offset of the follower or -1 if it is unknown"""
    last_fetch_timestamp: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The last known leader wall clock time time when a follower fetched from the leader. This is reported as -1 both for the current leader or if it is unknown for a voter"""
    last_caught_up_timestamp: i64 = field(
        metadata={"kafka_type": "int64"}, default=i64(-1)
    )
    """The leader wall clock append time of the offset for which the follower made the most recent fetch request. This is reported as the current time for the leader and -1 if unknown for a voter"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch"""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    current_voters: tuple[ReplicaState, ...]
    observers: tuple[ReplicaState, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeQuorumResponse:
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level error code."""
    topics: tuple[TopicData, ...]