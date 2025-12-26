from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from src.core.state import MonitoringState

SNAPSHOT_LOG_FILE = Path("data/monitor_snapshots.jsonl")


def build_snapshot(state: MonitoringState) -> str:
    """
    Constrói um mini-dashboard textual para exibir no terminal.
    """

    latest = state.latest_bucket()
    if not latest:
        return "No data in window yet."

    status = latest.status_counts

    window_size = state.window_size

    approved = status.get("approved", 0)
    failed = status.get("failed", 0)
    denied = status.get("denied", 0)
    reversed_ = status.get("reversed", 0)

    lines = [
        "========= SNAPSHOT =========",
        f"Window Size    : {window_size} minutes",
        f"Latest Minute  : {latest.timestamp}",
        "",
        f"Approved       : {approved}",
        f"Failed         : {failed}",
        f"Denied         : {denied}",
        f"Reversed       : {reversed_}",
        "============================",
    ]
    return "\n".join(lines)


def snapshot_to_dict(state: MonitoringState) -> Dict[str, Any]:
    """
    Versão estruturada do snapshot, para ser consumida pelo dashboard.

    Retorna um dicionário com:
    - timestamp
    - approved, failed, denied, reversed
    """

    latest = state.latest_bucket()
    if not latest:
        return {}

    status = latest.status_counts

    return {
        "timestamp": latest.timestamp.isoformat(),
        "approved": int(status.get("approved", 0)),
        "failed": int(status.get("failed", 0)),
        "denied": int(status.get("denied", 0)),
        "reversed": int(status.get("reversed", 0)),
    }


def append_snapshot_to_log(state: MonitoringState, path: Path = SNAPSHOT_LOG_FILE) -> None:
    """
    Acrescenta o snapshot atual em formato JSONL no arquivo.

    Cada linha do arquivo é um JSON independente.
    Isso facilita o Streamlit ler e montar gráficos em tempo quase real.
    """
    snap = snapshot_to_dict(state)
    if not snap:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")
