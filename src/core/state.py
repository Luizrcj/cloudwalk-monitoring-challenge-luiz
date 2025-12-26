from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class MinuteBucket:
    """
    Represents the aggregated view of the system for a single minute.

    - timestamp: minute bucket (normalized datetime)
    - status_counts: how many transactions by status in this minute
        e.g. {"approved": 120, "failed": 8, "denied": 5}
    - auth_code_counts: how many transactions by auth_code in this minute
        e.g. {0: 110, 1001: 8, 2002: 5}
    """
    timestamp: datetime
    status_counts: Dict[str, int] = field(default_factory=dict)
    auth_code_counts: Dict[int, int] = field(default_factory=dict)


@dataclass
class MonitoringState:
    """
    Holds the live state of the monitoring system.

    - window_size: how many last minutes we keep in memory
    - buckets: sliding window of MinuteBucket objects, ordered by time
    """
    window_size: int = 30
    buckets: List[MinuteBucket] = field(default_factory=list)

    def add_bucket(self, bucket: MinuteBucket) -> None:
        """
        Add a new minute snapshot to the state and enforce the sliding window.
        """
        self.buckets.append(bucket)
        # keep only the last `window_size` buckets
        if len(self.buckets) > self.window_size:
            # drop the oldest
            self.buckets = self.buckets[-self.window_size :]

    def latest_bucket(self) -> Optional[MinuteBucket]:
        """
        Returns the most recent minute snapshot, if any.
        """
        if not self.buckets:
            return None
        return self.buckets[-1]

    def status_series(self, status: str) -> List[int]:
        """
        Returns the time series (within the window) for a given status.
        Example: all 'failed' counts for the last N minutes.
        """
        return [b.status_counts.get(status, 0) for b in self.buckets]

    def auth_code_series(self, auth_code: int) -> List[int]:
        """
        Returns the time series for a specific authorization code.
        """
        return [b.auth_code_counts.get(auth_code, 0) for b in self.buckets]
    