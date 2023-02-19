"""
Generated from ElectLeadersRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartitions:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The name of a topic."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions of this topic whose leader should be elected."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ElectLeadersRequest:
    __flexible__: ClassVar[bool] = False
    topic_partitions: tuple[TopicPartitions, ...]
    """The topic partitions to elect leaders."""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """The time in ms to wait for the election to complete."""