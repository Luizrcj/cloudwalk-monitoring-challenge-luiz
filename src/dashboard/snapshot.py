from src.core.state import MonitoringState


def build_snapshot(state: MonitoringState) -> str:
    """
    Constrói um mini-dashboard textual do estado atual.

    Retorna uma string formatada para exibição no terminal.
    """

    latest = state.latest_bucket()
    if latest is None:
        return (
            "========= SNAPSHOT =========\n"
            "(sem dados ainda)\n"
            "============================"
        )

    status = latest.status_counts

    # tenta ler window_size se existir; se não, mostra "N/A"
    window_size = getattr(state, "window_size", "N/A")

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
