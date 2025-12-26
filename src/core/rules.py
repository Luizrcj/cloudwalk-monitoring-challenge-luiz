from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Tuple

from .state import MonitoringState, MinuteBucket


StatusType = Literal["approved", "failed", "denied", "reversed"]


@dataclass
class AnomalySignal:
    """
    Represents a potential anomaly detected by the monitoring rules.

    - timestamp: minute when the anomaly was observed
    - dimension: "status" or "auth_code"
    - key: e.g. "failed" or "auth_code=1001"
    - current_value: value in the latest minute
    - baseline_mean: average value in the recent history
    - baseline_std: standard deviation in the recent history
    - z_score: how many std deviations above the mean
    - reason: human-readable explanation (good for dashboards/logs)
    """
    timestamp: datetime
    dimension: str
    key: str
    current_value: int
    baseline_mean: float
    baseline_std: float
    z_score: float
    reason: str


def _compute_baseline(series: List[int]) -> Tuple[float, float]:
    """
    Computes simple mean and standard deviation for a series.
    Returns (mean, std). If the series is too small, returns (0.0, 0.0).
    """
    if not series:
        return 0.0, 0.0

    n = len(series)
    mean = sum(series) / n

    if n == 1:
        return mean, 0.0

    var = sum((x - mean) ** 2 for x in series) / (n - 1)
    std = var ** 0.5
    return mean, std


def detect_status_anomalies(
    state: MonitoringState,
    latest: MinuteBucket,
    watched_statuses: List[StatusType] = None,
    min_history: int = 10,
    z_threshold: float = 3.0,
    min_count: int = 5,
) -> List[AnomalySignal]:
    """
    Detects anomalies for transaction statuses (failed/denied/reversed, etc.)

    Rules:
    - only evaluate statuses with at least `min_history` points in the window
    - require current value >= `min_count` (avoid noise)
    - trigger when z-score > `z_threshold`
    """
    if watched_statuses is None:
        watched_statuses = ["failed", "denied", "reversed"]

    signals: List[AnomalySignal] = []

    for status in watched_statuses:
        series = state.status_series(status)

        # need enough history to build a baseline
        if len(series) < min_history:
            continue

        current_value = latest.status_counts.get(status, 0)
        mean, std = _compute_baseline(series)

        # no variability or very low baseline -> skip
        if std == 0 or mean == 0:
            continue

        if current_value < min_count:
            continue

        z = (current_value - mean) / std

        if z > z_threshold:
            signals.append(
                AnomalySignal(
                    timestamp=latest.timestamp,
                    dimension="status",
                    key=status,
                    current_value=current_value,
                    baseline_mean=mean,
                    baseline_std=std,
                    z_score=z,
                    reason=(
                        f"{status} spiked: {current_value} vs "
                        f"baseline mean={mean:.2f}, std={std:.2f}, z={z:.2f}"
                    ),
                )
            )

    return signals
