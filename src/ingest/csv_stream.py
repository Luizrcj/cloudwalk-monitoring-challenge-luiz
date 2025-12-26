import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, List

from src.core.state import MinuteBucket


def _parse_timestamp(value: str) -> datetime:
    """
    Parses timestamp from CSV.
    Expected format example:
        2024-01-01 10:05:00

    If format differs, adjust here.
    """
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def load_transactions_by_minute(file_path: Path) -> Dict[datetime, Dict[str, int]]:
    """
    Loads transactions.csv into a dictionary grouped by minute.

    Returns:
        {
            timestamp(datetime): {
                "approved": 120,
                "failed": 8,
                ...
            }
        }
    """
    grouped: Dict[datetime, Dict[str, int]] = {}

    with file_path.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = _parse_timestamp(row["timestamp"])
            status = row["status"].lower()
            count = int(row["count"])

            if ts not in grouped:
                grouped[ts] = {}

            grouped[ts][status] = count

    return grouped


def load_auth_codes_by_minute(file_path: Path) -> Dict[datetime, Dict[int, int]]:
    """
    Loads transactions_auth_codes.csv grouped by minute.

    Returns:
        {
            timestamp(datetime): {
                0: 110,
                1001: 5,
                2002: 3
            }
        }
    """
    grouped: Dict[datetime, Dict[int, int]] = {}

    with file_path.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = _parse_timestamp(row["timestamp"])
            auth_code = int(row["auth_code"])
            count = int(row["count"])

            if ts not in grouped:
                grouped[ts] = {}

            grouped[ts][auth_code] = count

    return grouped


def minute_stream(
    transactions_csv: Path,
    auth_codes_csv: Path,
) -> Iterator[MinuteBucket]:
    """
    Creates a unified time-ordered stream of MinuteBucket objects.

    It:
    - loads transactions by minute
    - loads auth codes by minute
    - merges both
    - yields one MinuteBucket per timestamp in ascending order
    """
    statuses = load_transactions_by_minute(transactions_csv)
    auth_codes = load_auth_codes_by_minute(auth_codes_csv)

    # unify the timeline
    all_timestamps: List[datetime] = sorted(
        set(statuses.keys()) | set(auth_codes.keys())
    )

    for ts in all_timestamps:
        bucket = MinuteBucket(
            timestamp=ts,
            status_counts=statuses.get(ts, {}),
            auth_code_counts=auth_codes.get(ts, {}),
        )
        yield bucket
