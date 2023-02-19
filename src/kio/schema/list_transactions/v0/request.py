"""
Generated from ListTransactionsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import ProducerId


@dataclass(frozen=True, slots=True, kw_only=True)
class ListTransactionsRequest:
    __flexible__: ClassVar[bool] = True
    state_filters: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The transaction states to filter by: if empty, all transactions are returned; if non-empty, then only transactions matching one of the filtered states will be returned"""
    producer_id_filters: tuple[ProducerId, ...] = field(
        metadata={"kafka_type": "int64"}, default=()
    )
    """The producerIds to filter by: if empty, all transactions will be returned; if non-empty, only transactions which match one of the filtered producerIds will be returned"""