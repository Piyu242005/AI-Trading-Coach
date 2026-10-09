"""Transparent, deterministic analytics for trade records.

These metrics describe historical records only; they are not predictions or financial advice.
"""
from __future__ import annotations

from typing import Any

import pandas as pd


def normalize_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with numeric P&L and consistent win/loss labels."""
    df = trades.copy()
    if df.empty:
        return df

    has_pnl = "pnl" in df.columns
    raw_pnl = pd.to_numeric(df["pnl"], errors="coerce") if has_pnl else pd.Series(index=df.index, dtype=float)
    has_observed_pnl = bool(raw_pnl.notna().any())
    df["pnl"] = raw_pnl.fillna(0.0)

    if has_observed_pnl:
        df["outcome"] = df["pnl"].map(
            lambda value: "win" if value > 0 else "loss" if value < 0 else "breakeven"
        )
    elif "outcome" in df.columns:
        normalized = df["outcome"].astype(str).str.strip().str.lower()
        df["outcome"] = normalized.where(
            normalized.isin(["win", "loss", "breakeven"]), "unknown"
        )
    else:
        df["outcome"] = "unknown"
    return df


def calculate_trade_metrics(trades: pd.DataFrame) -> dict[str, Any]:
    """Compute auditable trade-history metrics without inventing model performance."""
    df = normalize_trades(trades)
    if df.empty:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "breakeven": 0,
            "win_rate": 0.0,
            "total_pnl": 0.0,
            "average_pnl": 0.0,
            "profit_factor": None,
            "max_drawdown": 0.0,
        }

    pnl = df["pnl"]
    wins = int((df["outcome"] == "win").sum())
    losses = int((df["outcome"] == "loss").sum())
    breakeven = int((df["outcome"] == "breakeven").sum())
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else (None if gross_profit == 0 else float("inf"))
    )

    ordered = df
    if "entryAt" in df.columns:
        ordered = df.assign(
            _entry_at=pd.to_datetime(df["entryAt"], errors="coerce")
        ).sort_values("_entry_at", na_position="last")
    equity = ordered["pnl"].cumsum()
    drawdown = equity - equity.cummax().clip(lower=0)
    max_drawdown = float(abs(drawdown.min())) if not drawdown.empty else 0.0

    return {
        "total_trades": int(len(df)),
        "wins": wins,
        "losses": losses,
        "breakeven": breakeven,
        "win_rate": wins / len(df) * 100.0,
        "total_pnl": float(pnl.sum()),
        "average_pnl": float(pnl.mean()),
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
    }
