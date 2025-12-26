from pathlib import Path

from src.engine.monitor import run_monitoring_service


def main() -> None:
    """
    Entry point for the monitoring system.

    It wires:
    - data files
    - monitoring engine
    - configuration parameters (window, tick)
    """
    base_dir = Path(__file__).parent

    transactions_csv = base_dir / "data" / "transactions.csv"
    auth_codes_csv = base_dir / "data" / "transactions_auth_codes.csv"

    # basic safety check
    if not transactions_csv.exists():
        raise FileNotFoundError(f"transactions.csv not found at {transactions_csv}")
    if not auth_codes_csv.exists():
        raise FileNotFoundError(f"transactions_auth_codes.csv not found at {auth_codes_csv}")

    # configuration
    window_size_minutes = 30
    tick_seconds = 0.5  # each simulated "minute" will advance every 0.5s

    run_monitoring_service(
        transactions_csv=transactions_csv,
        auth_codes_csv=auth_codes_csv,
        window_size=window_size_minutes,
        tick_seconds=tick_seconds,
    )


if __name__ == "__main__":
    main()
