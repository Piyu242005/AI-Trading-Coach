def analyze_trader_behavior(user_id: str, trades: list) -> dict:
    # Filter trades for this user
    user_trades = [t for t in trades if str(t.get("userId")) == str(user_id)]

    if not user_trades:
        return {"userId": user_id, "behavior": "none", "evidence": []}

    # Group trades by sessionId for easier analysis
    sessions = {}
    for t in user_trades:
        sess_id = t.get("sessionId")
        if sess_id not in sessions:
            sessions[sess_id] = []
        sessions[sess_id].append(t)

    evidence = []
    detected_behavior = "none"

    for sess_id, st in sessions.items():
        # Sort session trades by entryAt time if possible
        # Simple format assumption: ISO strings
        try:
            st.sort(key=lambda x: x.get("entryAt", ""))
        except Exception:
            pass

        # Pattern 1: Overtrading (Rule: e.g., >= 5 trades in a single session)
        if len(st) >= 5:
            detected_behavior = "overtrading"
            evidence.append(
                {
                    "sessionId": sess_id,
                    "tradeIds": [t["tradeId"] for t in st],
                    "reason": f"{len(st)} trades detected in a single session",
                }
            )
            continue  # Prioritize overtrading reporting if multiple? Let's just break for simplicity right now

        # Pattern 2: FOMO (Rule: greedy or anxious emotional state)
        fomo_trades = [
            t for t in st if t.get("emotionalState") in ["greedy", "anxious"]
        ]
        if fomo_trades:
            detected_behavior = "FOMO"
            evidence.append(
                {
                    "sessionId": sess_id,
                    "tradeIds": [t["tradeId"] for t in fomo_trades],
                    "reason": f"Entered trades with {fomo_trades[0].get('emotionalState')} emotional state",
                }
            )

        # Pattern 3: Revenge Trading (Rule: loss -> next trade quickly or marked with revengeFlag)
        # Assuming the dataset has 'pnl' and 'revengeFlag'
        revenge_trades = [
            t
            for t in st
            if t.get("revengeFlag") is True or t.get("revengeFlag") == "true"
        ]
        if revenge_trades:
            detected_behavior = "revenge trading"
            evidence.append(
                {
                    "sessionId": sess_id,
                    "tradeIds": [t["tradeId"] for t in revenge_trades],
                    "reason": "Trades flagged as revenge or immediate post-loss entries",
                }
            )

    # Just an aggregate profile for the instructions
    return {"userId": user_id, "behavior": detected_behavior, "evidence": evidence}
