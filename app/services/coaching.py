from datetime import datetime
from typing import Any, Dict, List, Optional

OVERTRADING_THRESHOLD = 8
REVENGE_THRESHOLD = 2
REVENGE_WINDOW_MINUTES = 5
TILT_STREAK_THRESHOLD = 2

SIGNAL_PRIORITY = {
    "revenge_trading": 0,
    "session_tilt": 1,
    "overtrading": 2,
    "position_sizing_inconsistency": 3,
    "loss_running": 4,
    "premature_exit": 5,
    "fomo_entries": 6,
    "time_of_day_bias": 7,
    "plan_non_adherence": 8,
}


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _normalize_outcome(trade: Dict[str, Any]) -> str:
    return str(trade.get("outcome", "")).strip().lower()


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def _trade_id(trade: Dict[str, Any]) -> str:
    return str(trade.get("tradeId", "unknown"))


def _collect_user_trades(
    user_id: str, trades: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return [t for t in trades if str(t.get("userId")) == str(user_id)]


def _group_by_session(trades: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for trade in trades:
        session_id = str(trade.get("sessionId", "unknown"))
        grouped.setdefault(session_id, []).append(trade)

    for session_trades in grouped.values():
        session_trades.sort(key=lambda item: item.get("entryAt", ""))

    return grouped


def _detect_overtrading(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    if len(session_trades) <= OVERTRADING_THRESHOLD:
        return None

    trade_ids = [_trade_id(t) for t in session_trades]
    return {
        "signal": "overtrading",
        "sessionId": session_id,
        "tradeIds": trade_ids,
        "reason": (
            f"{len(session_trades)} trades in one session exceed the threshold "
            f"of {OVERTRADING_THRESHOLD}."
        ),
    }


def _detect_revenge_trading(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    revenge_ids = {
        _trade_id(t) for t in session_trades if _normalize_bool(t.get("revengeFlag"))
    }

    for index in range(1, len(session_trades)):
        previous_trade = session_trades[index - 1]
        current_trade = session_trades[index]
        if _normalize_outcome(previous_trade) != "loss":
            continue

        previous_exit = _parse_iso(previous_trade.get("exitAt"))
        current_entry = _parse_iso(current_trade.get("entryAt"))
        if previous_exit is None or current_entry is None:
            continue

        delta_minutes = (current_entry - previous_exit).total_seconds() / 60.0
        if 0 <= delta_minutes <= REVENGE_WINDOW_MINUTES:
            revenge_ids.add(_trade_id(current_trade))

    if len(revenge_ids) < REVENGE_THRESHOLD:
        return None

    sorted_ids = sorted(revenge_ids)
    return {
        "signal": "revenge_trading",
        "sessionId": session_id,
        "tradeIds": sorted_ids,
        "reason": (
            f"{len(sorted_ids)} trades were flagged as revenge or opened within "
            f"{REVENGE_WINDOW_MINUTES} minutes after a loss."
        ),
    }


def _is_tilt_trade(trade: Dict[str, Any]) -> bool:
    outcome_is_loss = _normalize_outcome(trade) == "loss"
    emotional_state = str(trade.get("emotionalState", "")).strip().lower()
    emotional_tilt = emotional_state in {"anxious", "fearful"}

    try:
        adherence = float(trade.get("planAdherence", 0))
    except (TypeError, ValueError):
        adherence = 0

    return outcome_is_loss and emotional_tilt and adherence <= 2


def _detect_tilt(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    current_streak: List[str] = []
    longest_streak: List[str] = []

    for trade in session_trades:
        if _is_tilt_trade(trade):
            current_streak.append(_trade_id(trade))
            if len(current_streak) > len(longest_streak):
                longest_streak = list(current_streak)
        else:
            current_streak = []

    if len(longest_streak) < TILT_STREAK_THRESHOLD:
        return None

    return {
        "signal": "session_tilt",
        "sessionId": session_id,
        "tradeIds": longest_streak,
        "reason": (
            "Consecutive loss trades occurred with anxious/fearful state and low "
            "plan adherence (<= 2)."
        ),
    }


def _detect_fomo(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    fomo_ids = [
        _trade_id(t)
        for t in session_trades
        if "catch the rest" in str(t.get("entryRationale", "")).lower()
        or str(t.get("emotionalState", "")).lower() == "greedy"
    ]
    if not fomo_ids:
        return None
    return {
        "signal": "fomo_entries",
        "sessionId": session_id,
        "tradeIds": fomo_ids,
        "reason": "Entry rationale indicates late entry driven by fear of missing out.",
    }


def _detect_plan_non_adherence(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    try:
        non_adherent_ids = [
            _trade_id(t)
            for t in session_trades
            if float(t.get("planAdherence", 5)) <= 2
        ]
    except (TypeError, ValueError):
        non_adherent_ids = []
    if len(non_adherent_ids) < len(session_trades) * 0.5 or not session_trades:
        return None
    return {
        "signal": "plan_non_adherence",
        "sessionId": session_id,
        "tradeIds": non_adherent_ids,
        "reason": "Majority of trades in this session severely deviated from the trading plan.",
    }


def _detect_premature_exit(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    premature_ids = [
        _trade_id(t)
        for t in session_trades
        if "fear of reversal" in str(t.get("entryRationale", "")).lower()
    ]
    if not premature_ids:
        return None
    return {
        "signal": "premature_exit",
        "sessionId": session_id,
        "tradeIds": premature_ids,
        "reason": "Trades were exited early out of fear, cutting potential profits short.",
    }


def _detect_loss_running(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    loss_running_ids = [
        _trade_id(t)
        for t in session_trades
        if "hop" in str(t.get("entryRationale", "")).lower()
        and _normalize_outcome(t) == "loss"
    ]
    if not loss_running_ids:
        return None
    return {
        "signal": "loss_running",
        "sessionId": session_id,
        "tradeIds": loss_running_ids,
        "reason": "Losing trades were held open based on hope rather than technical rules.",
    }


def _detect_time_of_day_bias(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    afternoon_losses = []
    for t in session_trades:
        if _normalize_outcome(t) == "loss" and t.get("entryAt"):
            dt = _parse_iso(t.get("entryAt"))
            if dt and dt.hour >= 13:
                afternoon_losses.append(_trade_id(t))
    if len(afternoon_losses) < 3:
        return None
    return {
        "signal": "time_of_day_bias",
        "sessionId": session_id,
        "tradeIds": afternoon_losses,
        "reason": "Consistent pattern of losses occurring during afternoon trading hours.",
    }


def _detect_position_sizing(
    session_id: str, session_trades: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    inconsistent_ids = []
    prev_qty = None
    prev_outcome = None
    for t in session_trades:
        try:
            qty = float(t.get("quantity", 0))
        except (TypeError, ValueError):
            qty = 0
        if prev_qty and prev_outcome == "win" and qty >= prev_qty * 5:
            inconsistent_ids.append(_trade_id(t))
        prev_qty = qty
        prev_outcome = _normalize_outcome(t)
    if not inconsistent_ids:
        return None
    return {
        "signal": "position_sizing_inconsistency",
        "sessionId": session_id,
        "tradeIds": inconsistent_ids,
        "reason": "Massive position size increases detected following winning trades.",
    }


def detect_signals_for_user_trades(
    user_id: str, trades: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    user_trades = _collect_user_trades(user_id, trades)
    grouped = _group_by_session(user_trades)

    ordered_sessions = sorted(
        grouped.items(),
        key=lambda item: (
            item[1][0].get("entryAt", "") if item[1] else "",
            item[0],
        ),
    )

    detected: List[Dict[str, Any]] = []
    for session_id, session_trades in ordered_sessions:
        overtrading = _detect_overtrading(session_id, session_trades)
        if overtrading is not None:
            detected.append(overtrading)

        revenge = _detect_revenge_trading(session_id, session_trades)
        if revenge is not None:
            detected.append(revenge)

        tilt = _detect_tilt(session_id, session_trades)
        if tilt is not None:
            detected.append(tilt)

        fomo = _detect_fomo(session_id, session_trades)
        if fomo is not None:
            detected.append(fomo)

        pna = _detect_plan_non_adherence(session_id, session_trades)
        if pna is not None:
            detected.append(pna)

        premature = _detect_premature_exit(session_id, session_trades)
        if premature is not None:
            detected.append(premature)

        loss_running = _detect_loss_running(session_id, session_trades)
        if loss_running is not None:
            detected.append(loss_running)

        tod = _detect_time_of_day_bias(session_id, session_trades)
        if tod is not None:
            detected.append(tod)

        pos_sizing = _detect_position_sizing(session_id, session_trades)
        if pos_sizing is not None:
            detected.append(pos_sizing)

    detected.sort(
        key=lambda signal: (
            SIGNAL_PRIORITY.get(signal["signal"], 99),
            signal["sessionId"],
        )
    )
    return detected


def build_coaching_message(user_id: str, signals: List[Dict[str, Any]]) -> str:
    if not signals:
        return (
            f"No overtrading, tilt, or revenge trading signal was detected for user {user_id} "
            "from the provided trades."
        )

    primary = signals[0]
    session_id = primary["sessionId"]
    trade_ids = ", ".join(primary["tradeIds"])
    trade_count = len(primary["tradeIds"])

    if primary["signal"] == "revenge_trading":
        return (
            f"You placed {trade_count} trades after losses in session {session_id} "
            f"(tradeIds: {trade_ids}). This indicates revenge trading. Pause and reassess."
        )

    if primary["signal"] == "session_tilt":
        return (
            f"In session {session_id}, trades {trade_ids} show a loss streak with anxious/fearful "
            "state and low plan adherence. This indicates tilt. Step away and reset your rules."
        )

    if primary["signal"] == "overtrading":
        return (
            f"Session {session_id} contains {trade_count} trades (tradeIds: {trade_ids}), which exceeds "
            "the overtrading threshold. Slow down and wait for higher-conviction setups."
        )

    return f"Detected {primary['signal']} in session {session_id} across {trade_count} trades (tradeIds: {trade_ids}). {primary['reason']}"


def tokenize_message(message: str) -> List[str]:
    return message.split(" ")
