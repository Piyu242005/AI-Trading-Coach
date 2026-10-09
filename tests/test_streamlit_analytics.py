from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "frontend-streamlit"))
from analytics import calculate_trade_metrics, normalize_trades  # noqa: E402


def test_empty_trades_have_safe_zero_metrics():
    metrics = calculate_trade_metrics(pd.DataFrame())
    assert metrics["total_trades"] == 0
    assert metrics["win_rate"] == 0
    assert metrics["profit_factor"] is None


def test_metrics_are_derived_from_real_pnl():
    df = pd.DataFrame({"pnl": [100, -40, 0, 60], "entryAt": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]})
    metrics = calculate_trade_metrics(df)
    assert metrics["total_trades"] == 4
    assert metrics["wins"] == 2
    assert metrics["losses"] == 1
    assert metrics["breakeven"] == 1
    assert metrics["win_rate"] == 50
    assert metrics["total_pnl"] == 120
    assert metrics["profit_factor"] == 4
    assert metrics["max_drawdown"] == 40


def test_invalid_pnl_is_coerced_and_outcome_is_normalized():
    df = normalize_trades(pd.DataFrame({"pnl": ["10", "bad", "-2"], "outcome": ["WIN", "unknown", "loss"]}))
    assert df["pnl"].tolist() == [10.0, 0.0, -2.0]
    assert df["outcome"].tolist() == ["win", "breakeven", "loss"]
