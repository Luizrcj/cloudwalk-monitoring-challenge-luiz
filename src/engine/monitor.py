from pathlib import Path
from time import sleep
from typing import Iterable, List

from src.core.state import MonitoringState, MinuteBucket
from src.core.rules import detect_status_anomalies, AnomalySignal
from src.ingest.csv_stream import minute_stream
from src.alerting.alerts import handle_alerts
from src.dashboard.snapshot import build_snapshot


def run_monitoring_service(
    transactions_csv: Path,
    auth_codes_csv: Path,
    window_size: int = 30,
    tick_seconds: float = 1.0,
) -> None:
    """
    Main monitoring loop.

    Responsibilities:
    - Create monitoring state
    - Stream minute buckets in chronological order
    - Update state with each new bucket
    - Evaluate anomaly rules
    - Trigger alert handling when needed
    """

    print("🚀 Monitoring service starting...")
    print(f"Window size = last {window_size} minutes")
    print(f"Tick = {tick_seconds} seconds per simulated minute")
    print("--------------------------------------------------")

    state = MonitoringState(window_size=window_size)

    stream = minute_stream(transactions_csv, auth_codes_csv)

    for bucket in stream:
        _process_minute(state, bucket)

        # simulate real-time progression
        sleep(tick_seconds)


def _process_minute(state: MonitoringState, bucket: MinuteBucket) -> None:
    """
    Handles one monitoring cycle for a single minute.
    """
    print(f"\n📡 Processing minute -> {bucket.timestamp}")

    # update sliding window
    state.add_bucket(bucket)

    # latest state snapshot
    latest = state.latest_bucket()
    if not latest:
        return

    # build dashboard snapshot
    from src.dashboard.snapshot import build_snapshot
    snapshot = build_snapshot(state)
    print(snapshot)

    # run anomaly detection
    signals: List[AnomalySignal] = detect_status_anomalies(
        state=state,
        latest=latest,
    )

    if not signals:
        print("✅ No anomalies detected.")
        return

    print(f"⚠️  {len(signals)} anomaly signal(s) detected!")
    handle_alerts(signals)