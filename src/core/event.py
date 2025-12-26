from dataclasses import dataclass
from datetime import datetime


@dataclass
class TransactionStatusEvent:
    """
    Represents aggregated transaction status per minute.

    Maps to transactions.csv:
        timestamp -> minute bucket
        status    -> approved / failed / denied / reversed / etc
        count     -> total transactions of this status in that minute
    """
    timestamp: datetime
    status: str
    count: int


@dataclass
class TransactionAuthCodeEvent:
    """
    Represents aggregated authorization codes per minute.

    Maps to transactions_auth_codes.csv:
        timestamp -> minute bucket
        auth_code -> numeric authorization code
        count     -> volume of transactions for that code in that minute
    """
    timestamp: datetime
    auth_code: int
    count: int
    