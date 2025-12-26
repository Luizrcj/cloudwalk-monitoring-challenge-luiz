import json
import time
from pathlib import Path

import pandas as pd
import streamlit as st

SNAPSHOT_LOG_FILE = Path("data/monitor_snapshots.jsonl")


def load_snapshots():
    if not SNAPSHOT_LOG_FILE.exists():
        return pd.DataFrame()

    rows = []
    with SNAPSHOT_LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # ignora linhas quebradas
                continue

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"])
    return df


def main():
    st.set_page_config(
        page_title="CloudWalk – Real-Time Monitoring Dashboard",
        layout="wide",
    )

    st.title("CloudWalk – Real-Time Transactions Monitoring")
    st.caption("Dashboard em tempo quase real baseado no engine de monitoramento em Python.")

    placeholder = st.empty()

    while True:
        df = load_snapshots()

        if df.empty:
            placeholder.info(
                "Aguardando snapshots... "
                "Certifique-se de que o serviço de monitoramento (`python main.py`) está em execução."
            )
        else:
            latest = df.iloc[-1]

            with placeholder.container():
                st.subheader("Último snapshot")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Approved", int(latest["approved"]))
                c2.metric("Failed", int(latest["failed"]))
                c3.metric("Denied", int(latest["denied"]))
                c4.metric("Reversed", int(latest["reversed"]))

                st.markdown("---")

                st.subheader("Evolução por status (janela completa)")

                chart_df = df.set_index("timestamp")[["approved", "failed", "denied", "reversed"]]
                st.line_chart(chart_df)

        # intervalo de atualização (2 segundos)
        time.sleep(2)


if __name__ == "__main__":
    main()
