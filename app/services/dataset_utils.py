from typing import Any, Dict, List, Set


def get_traders(dataset: Any) -> List[Dict[str, Any]]:
    if isinstance(dataset, dict):
        traders = dataset.get("traders", [])
        return traders if isinstance(traders, list) else []
    return []


def flatten_all_trades(dataset: Any) -> List[Dict[str, Any]]:
    trades: List[Dict[str, Any]] = []
    for trader in get_traders(dataset):
        sessions = trader.get("sessions", [])
        if not isinstance(sessions, list):
            continue
        for session in sessions:
            session_trades = session.get("trades", [])
            if not isinstance(session_trades, list):
                continue
            trades.extend(session_trades)
    return trades


def flatten_user_trades(dataset: Any, user_id: str) -> List[Dict[str, Any]]:
    user_trades: List[Dict[str, Any]] = []
    for trader in get_traders(dataset):
        if str(trader.get("userId")) != str(user_id):
            continue
        sessions = trader.get("sessions", [])
        if not isinstance(sessions, list):
            continue
        for session in sessions:
            session_trades = session.get("trades", [])
            if isinstance(session_trades, list):
                user_trades.extend(session_trades)
    return user_trades


def get_user_session_ids(dataset: Any, user_id: str) -> Set[str]:
    session_ids: Set[str] = set()
    for trader in get_traders(dataset):
        if str(trader.get("userId")) != str(user_id):
            continue
        sessions = trader.get("sessions", [])
        if not isinstance(sessions, list):
            continue
        for session in sessions:
            session_id = session.get("sessionId")
            if session_id is not None:
                session_ids.add(str(session_id))
    return session_ids


def get_ground_truth_map(dataset: Any) -> Dict[str, Set[str]]:
    labels_map: Dict[str, Set[str]] = {}
    if not isinstance(dataset, dict):
        return labels_map

    labels = dataset.get("groundTruthLabels", [])
    if not isinstance(labels, list):
        return labels_map

    for row in labels:
        user_id = str(row.get("userId", ""))
        pathologies = row.get("pathologies", [])
        if not user_id:
            continue
        if not isinstance(pathologies, list):
            pathologies = []
        labels_map[user_id] = {str(item) for item in pathologies}

    return labels_map
