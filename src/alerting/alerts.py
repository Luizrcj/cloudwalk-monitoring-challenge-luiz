from typing import List
from datetime import datetime

from src.core.rules import AnomalySignal


def handle_alerts(signals: List[AnomalySignal]) -> None:
    """
    Central alert dispatcher.
    Today it only prints structured alerts.

    In a real-world setup, this function could:
    - send Slack notifications
    - trigger PagerDuty incidents
    - push events to an alerting platform
    - write to a monitoring log pipeline
    """
    for signal in signals:
        _print_alert(signal)


def _print_alert(signal: AnomalySignal) -> None:
    """
    Human-friendly alert output.

    This makes the system explainable
    and showcases clarity in interviews.
    """
    print(
        "\n🚨 ALERT DETECTED 🚨\n"
        f"Time: {signal.timestamp}\n"
        f"Dimension: {signal.dimension}\n"
        f"Key: {signal.key}\n"
        f"Current Value: {signal.current_value}\n"
        f"Baseline Mean: {signal.baseline_mean:.2f}\n"
        f"Baseline Std: {signal.baseline_std:.2f}\n"
        f"Z-Score: {signal.z_score:.2f}\n"
        f"Reason: {signal.reason}\n"
        "----------------------------------------------"
    )
