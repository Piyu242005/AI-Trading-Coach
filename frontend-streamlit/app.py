import datetime
from typing import Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import joblib
import shap
import numpy as np
import os
from pathlib import Path

from analytics import calculate_trade_metrics, normalize_trades

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.jpg"
MODEL_DIR = BASE_DIR / "models"
DEFAULT_API_URL = os.getenv("AI_TRADING_COACH_API_URL", "https://ai-trading-coach-2vao.onrender.com").rstrip("/")

st.set_page_config(page_title="AI Trading Coach", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

def apply_editorial_theme() -> None:
    """Apply the Editorial FinTech design system across the Streamlit application."""
    st.markdown(
        """
        <style>
        :root {
          color-scheme: light;
          --paper: #F4F1E8;
          --surface: #FFFEFA;
          --forest: #174C3C;
          --ink: #202820;
          --muted: #687067;
          --amber: #E8A15A;
          --line: #DED9CD;
          --loss: #B54742;
        }
        .stApp { background: var(--paper); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(244, 241, 232, .94); }
        [data-testid="stSidebar"] {
          background: #EAE6DA;
          border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] > div { padding-top: 1.25rem; }
        .block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 3rem; }
        h1, h2, h3 {
          color: var(--ink) !important;
          font-family: Georgia, "Times New Roman", serif !important;
          letter-spacing: -.035em !important;
        }
        h1 { font-size: clamp(2.1rem, 4vw, 3.6rem) !important; line-height: 1.04 !important; }
        h2 { font-size: clamp(1.55rem, 2.4vw, 2.2rem) !important; }
        h3 { font-size: 1.35rem !important; }
        p, label, .stMarkdown, .stCaption, [data-testid="stWidgetLabel"] {
          color: var(--ink);
          font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
        [data-testid="stMetric"] {
          background: var(--surface); border: 1px solid var(--line);
          padding: 1.1rem 1.15rem; border-radius: 14px; box-shadow: 0 3px 14px rgba(32,40,32,.025);
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .78rem; text-transform: uppercase; letter-spacing: .07em; }
        [data-testid="stMetricValue"] { color: var(--forest) !important; font-family: "SFMono-Regular", Consolas, monospace; font-size: clamp(1.35rem, 2vw, 2rem); }
        .stButton > button, .stFormSubmitButton > button {
          border-radius: 9px; min-height: 2.75rem; font-weight: 650;
          border: 1px solid var(--forest); transition: transform .16s ease, box-shadow .16s ease;
        }
        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
          background: var(--forest); color: #fffdf7;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
          transform: translateY(-1px); box-shadow: 0 5px 16px rgba(23,76,60,.12); border-color: var(--forest);
        }
        input, textarea, [data-baseweb="select"] > div {
          background: var(--surface) !important; border-color: var(--line) !important; border-radius: 8px !important;
        }
        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
          background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden;
        }
        [data-testid="stAlert"] { border-radius: 10px; }
        hr { border-color: var(--line); }
        .editorial-kicker { color: var(--forest); font-size: .72rem; font-weight: 750; letter-spacing: .16em; text-transform: uppercase; }
        .editorial-panel { background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 1.25rem; }
        .editorial-note { color: var(--muted); font-size: .88rem; line-height: 1.55; }
        @media (max-width: 768px) {
          .block-container { padding: 1.2rem 1rem 2rem; }
          [data-testid="stMetric"] { padding: .8rem; }
          [data-testid="stMetricValue"] { font-size: 1.25rem; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig, height: int | None = None):
    """Keep Plotly charts visually consistent with the editorial paper palette."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFEFA",
        plot_bgcolor="#FFFEFA",
        font={"family": "Inter, Arial, sans-serif", "color": "#202820", "size": 12},
        margin={"l": 18, "r": 18, "t": 32, "b": 18},
        hoverlabel={"bgcolor": "#202820", "font_color": "#FFFEFA"},
        legend={"bgcolor": "rgba(255,254,250,0)", "font": {"color": "#202820"}},
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E9E5DA", zerolinecolor="#DED9CD")
    fig.update_yaxes(showgrid=True, gridcolor="#E9E5DA", zerolinecolor="#DED9CD")
    if height:
        fig.update_layout(height=height)
    return fig



def init_session_state() -> None:
    defaults = {
        "token": None,
        "user_id": "guest_demo",
        "is_guest": True,
        "welcome_screen_passed": False,
        "trades_data": [],
        "journal_entries": [],
        "coach_messages": [],
        "api_url": DEFAULT_API_URL,
        "discipline_score": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
    # Force fix if stuck on old localhost from previous session
    if st.session_state.get("api_url") == "http://localhost:8000":
        st.session_state["api_url"] = DEFAULT_API_URL


def get_api_url() -> str:
    return str(st.session_state.api_url).rstrip("/")


def api_headers() -> Dict[str, str]:
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login(user_id: str, password: str) -> None:
    try:
        response = requests.post(
            f"{get_api_url()}/api/auth/token", json={"userId": user_id, "password": password}, timeout=10
        )
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.session_state.user_id = user_id
            st.session_state.is_guest = False
            st.session_state.welcome_screen_passed = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error(f"Login failed (HTTP {response.status_code}). Check the credentials and backend authentication configuration.")
    except requests.RequestException:
        st.error("Could not reach the API. Check the service status and try again.")


def load_user_trades(force: bool = False) -> None:
    if st.session_state.trades_data and not force:
        return

    if st.session_state.user_id == "guest_demo":
        st.session_state.trades_data = [
            {"tradeId": "t1", "asset": "AAPL", "assetClass": "Equities", "direction": "Long", "entryPrice": 150, "exitPrice": 155, "pnl": 500, "entryAt": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(), "outcome": "win"},
            {"tradeId": "t2", "asset": "TSLA", "assetClass": "Equities", "direction": "Short", "entryPrice": 200, "exitPrice": 210, "pnl": -1000, "entryAt": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(), "outcome": "loss"},
            {"tradeId": "t3", "asset": "BTC", "assetClass": "Crypto", "direction": "Long", "entryPrice": 60000, "exitPrice": 62000, "pnl": 2000, "entryAt": (datetime.datetime.now() - datetime.timedelta(hours=5)).isoformat(), "outcome": "win"},
            {"tradeId": "t4", "asset": "ETH", "assetClass": "Crypto", "direction": "Long", "entryPrice": 3000, "exitPrice": 3100, "pnl": 500, "entryAt": (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(), "outcome": "win"},
            {"tradeId": "t5", "asset": "NIFTY", "assetClass": "Indices", "direction": "Long", "entryPrice": 20000, "exitPrice": 20200, "pnl": 1000, "entryAt": (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat(), "outcome": "win"},
        ]
        return

    try:
        response = requests.get(f"{get_api_url()}/api/trades", headers=api_headers(), timeout=10)
        if response.status_code != 200:
            st.error("Failed to load trades from backend.")
            return

        data = response.json()
        traders = data.get("traders", [])

        all_trades = []
        for trader in traders:
            if str(trader.get("userId")) == str(st.session_state.user_id):
                for session in trader.get("sessions", []):
                    all_trades.extend(session.get("trades", []))

        st.session_state.trades_data = all_trades
    except requests.RequestException:
        st.error("Could not load trades. Check the API service status and try again.")






def build_trade_frame(trades: List[Dict[str, object]]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()

    df = pd.DataFrame(trades)
    if "entryAt" in df.columns:
        df["entryAt"] = pd.to_datetime(df["entryAt"], errors="coerce")
    if "exitAt" in df.columns:
        df["exitAt"] = pd.to_datetime(df["exitAt"], errors="coerce")
    for col in ["pnl", "entryPrice", "exitPrice"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "pnl" not in df.columns:
        df["pnl"] = 0
    if "outcome" not in df.columns:
        df["outcome"] = df["pnl"].apply(lambda value: "win" if value > 0 else "loss" if value < 0 else "breakeven")
    return df


def compute_summary_metrics(df: pd.DataFrame) -> Dict[str, object]:
    """Compatibility wrapper around the tested analytics module."""
    return calculate_trade_metrics(df)



def build_price_series(df: pd.DataFrame, asset: str) -> pd.DataFrame:
    """Build a price series only from recorded trade prices; never fabricate market data."""
    if df.empty or "entryAt" not in df.columns:
        return pd.DataFrame(columns=["date", "price"])
    selected = df[df["asset"].astype(str) == str(asset)].copy() if "asset" in df.columns else df.copy()
    selected["date"] = pd.to_datetime(selected["entryAt"], errors="coerce")
    selected = selected.dropna(subset=["date"])
    price_column = next((name for name in ["entryPrice", "exitPrice"] if name in selected.columns and pd.to_numeric(selected[name], errors="coerce").notna().any()), None)
    if price_column is None:
        return pd.DataFrame(columns=["date", "price"])
    selected["price"] = pd.to_numeric(selected[price_column], errors="coerce")
    return selected.dropna(subset=["price"])[["date", "price"]].sort_values("date")



def render_dashboard(df: pd.DataFrame) -> None:
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=58)
    with col_title:
        st.title("Trading Intelligence Dashboard")
        st.caption("Historical trade analytics • Transparent calculations • Demo data clearly labeled")
    if st.session_state.is_guest:
        st.info("Demo mode: sample trades are illustrative, not live market data or personal trading history.")
    if df.empty:
        st.warning("No trade records are available yet. Add or import trades to calculate portfolio statistics.")
        return

    metrics = calculate_trade_metrics(df)
    factor = metrics["profit_factor"]
    factor_label = "∞" if factor == float("inf") else "—" if factor is None else f'{factor:.2f}x'
    total_pnl = metrics["total_pnl"]
    prefix = "+" if total_pnl > 0 else ""
    cards = st.columns(5)
    cards[0].metric("Trades", f'{metrics["total_trades"]:,}')
    cards[1].metric("Win rate", f'{metrics["win_rate"]:.1f}%')
    cards[2].metric("Net P&L", f'{prefix}${total_pnl:,.2f}')
    cards[3].metric("Profit factor", factor_label)
    cards[4].metric("Max drawdown", f'₹{metrics["max_drawdown"]:,.2f}')

    st.divider()
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.subheader("Cumulative P&L")
        ordered = df.copy()
        if "entryAt" in ordered.columns:
            ordered["entryAt"] = pd.to_datetime(ordered["entryAt"], errors="coerce")
            ordered = ordered.sort_values("entryAt", na_position="last")
        if "pnl" not in ordered.columns:
            ordered["pnl"] = 0.0
        ordered["pnl"] = pd.to_numeric(ordered["pnl"], errors="coerce").fillna(0)
        ordered["Cumulative P&L"] = ordered["pnl"].cumsum()
        if "entryAt" in ordered.columns and ordered["entryAt"].notna().any():
            fig = px.line(ordered, x="entryAt", y="Cumulative P&L", template="plotly_white")
            fig.update_layout(margin=dict(l=12, r=12, t=24, b=12), height=330, xaxis_title="Trade date", yaxis_title="P&L")
            st.plotly_chart(style_figure(fig), use_container_width=True)
        else:
            st.caption("Add valid trade dates to display the cumulative P&L timeline.")
    with right:
        st.subheader("Trade outcomes")
        counts = normalize_trades(df)["outcome"].value_counts().rename_axis("Outcome").reset_index(name="Trades")
        fig = px.pie(counts, names="Outcome", values="Trades", hole=0.62, template="plotly_white")
        fig.update_layout(margin=dict(l=8, r=8, t=24, b=8), height=330, legend_title_text="")
        st.plotly_chart(style_figure(fig), use_container_width=True)
        st.caption(f'{metrics["wins"]} wins · {metrics["losses"]} losses · {metrics["breakeven"]} breakeven')
    st.subheader("Trade history")
    columns = [c for c in ["entryAt", "asset", "direction", "entryPrice", "exitPrice", "pnl", "outcome"] if c in df.columns]
    st.dataframe(df[columns] if columns else df, use_container_width=True, hide_index=True)




def render_ai_coach(df: pd.DataFrame) -> None:
    st.header("Trading Insights Coach")
    st.caption("Deterministic insights from your trade records; this version does not call an external LLM.")
    st.info("Educational analytics only—not investment advice or a promise of future performance.")
    tab_chat, tab_review = st.tabs(["Ask about my trades", "Review a trade"])
    with tab_chat:
        if not st.session_state.coach_messages:
            st.session_state.coach_messages.append({"role": "assistant", "content": "Ask about win rate, losses, P&L, or assets in your recorded trades."})
        for message in st.session_state.coach_messages:
            with st.chat_message(message["role"], avatar=str(LOGO_PATH) if message["role"] == "assistant" and LOGO_PATH.exists() else None):
                st.write(message["content"])
        prompt = st.chat_input("Ask about your recorded trades…")
        if prompt:
            st.session_state.coach_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            if df.empty:
                reply = "There are no trade records to analyze yet. Add or import trades first."
            else:
                m = calculate_trade_metrics(df)
                normalized = normalize_trades(df)
                q = prompt.casefold()
                if "win rate" in q or "winning" in q:
                    reply = f'Your recorded win rate is {m["win_rate"]:.1f}% ({m["wins"]} wins out of {m["total_trades"]} trades). This is historical performance, not a forecast.'
                elif "loss" in q or "drawdown" in q or "risk" in q:
                    reply = f'Your recorded net P&L is ${m["total_pnl"]:,.2f}; maximum peak-to-trough drawdown from ordered trade P&L is ${m["max_drawdown"]:,.2f}. Review position sizing and stop rules before making trading decisions.'
                elif "best" in q or "asset" in q or "symbol" in q:
                    if "asset" in normalized.columns:
                        by_asset = normalized.groupby("asset", dropna=True)["pnl"].sum().sort_values(ascending=False)
                        reply = "Net P&L by asset in the recorded data:\n" + "\n".join(f"• {asset}: ${value:,.2f}" for asset, value in by_asset.items()) if not by_asset.empty else "The records do not contain asset names to compare."
                    else:
                        reply = "The records do not contain an asset column to compare."
                elif "profit factor" in q:
                    f = m["profit_factor"]
                    text_factor = "undefined" if f is None else "infinite (no gross losses)" if f == float("inf") else f"{f:.2f}"
                    reply = f"Your historical profit factor is {text_factor}. It does not establish future profitability."
                else:
                    reply = f'From {m["total_trades"]} recorded trades, net P&L is ${m["total_pnl"]:,.2f}, average P&L per trade is ${m["average_pnl"]:,.2f}, and win rate is {m["win_rate"]:.1f}%. Ask about win rate, losses/drawdown, assets, or profit factor.'
            st.session_state.coach_messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant", avatar=str(LOGO_PATH) if LOGO_PATH.exists() else None):
                st.write(reply)
    with tab_review:
        if df.empty:
            st.warning("No trades are available to review.")
        elif "asset" not in df.columns:
            st.warning("Trade records need an asset column to select a trade.")
        else:
            review_df = df.reset_index(drop=True).copy()
            labels = [f'{i + 1}. {row.get("direction", "Trade")} {row.get("asset", "Unknown")} · {str(row.get("entryAt", "date unavailable"))[:10]} · P&L {float(row.get("pnl", 0) or 0):,.2f}' for i, row in review_df.iterrows()]
            selected = st.selectbox("Choose a recorded trade", range(len(labels)), format_func=lambda idx: labels[idx])
            row = review_df.iloc[selected]
            pnl = float(row.get("pnl", 0) or 0)
            st.subheader("Record-based review")
            st.metric("Recorded P&L", f'{"+" if pnl > 0 else ""}{pnl:,.2f}')
            st.write(f'**Asset:** {row.get("asset", "Not recorded")}')
            st.write(f'**Direction:** {row.get("direction", "Not recorded")}')
            st.write(f'**Entry:** {row.get("entryPrice", "Not recorded")} · **Exit:** {row.get("exitPrice", "Not recorded")}')
            st.write(f'**Outcome:** {row.get("outcome", "Not recorded")}')
            st.caption("This summarizes recorded fields only. It does not infer unrecorded stop-losses, emotions, entry conditions, or reasons for the outcome.")




def render_market_analysis(df: pd.DataFrame) -> None:
    st.header("Market & Trade History Analysis")
    st.caption("Charts use recorded trade prices only. No synthetic or live market prices are substituted.")
    if df.empty or "asset" not in df.columns:
        st.warning("No asset history is available. Add or import trade records with asset and price fields.")
        return
    assets = sorted(str(asset) for asset in df["asset"].dropna().unique())
    if not assets:
        st.warning("No valid asset symbols were found in the records.")
        return
    asset = st.selectbox("Asset", assets)
    series = build_price_series(df, asset)
    if series.empty or "price" not in series.columns:
        st.warning(f"No recorded entry or exit prices with valid dates are available for {asset}.")
        return
    series = series.copy()
    series["price"] = pd.to_numeric(series["price"], errors="coerce")
    series = series.dropna(subset=["price"]).sort_values("date")
    if series.empty:
        st.warning("The selected asset has no usable price values.")
        return
    series["moving_average"] = series["price"].rolling(window=min(5, len(series)), min_periods=1).mean()
    series["returns"] = series["price"].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
    series["volatility"] = series["returns"].rolling(window=min(5, len(series)), min_periods=2).std().fillna(0) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series["date"], y=series["price"], name="Recorded price", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=series["date"], y=series["moving_average"], name="Rolling average", mode="lines"))
    fig.update_layout(template="plotly_white", height=380, margin=dict(l=12, r=12, t=24, b=12), xaxis_title="Recorded date", yaxis_title="Price")
    st.plotly_chart(style_figure(fig), use_container_width=True)
    st.caption("Rolling average and volatility describe the available trade-price records; they are not live technical signals.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Observed price variation")
        fig_vol = px.area(series, x="date", y="volatility", labels={"volatility": "Rolling variation (%)"}, template="plotly_white")
        st.plotly_chart(style_figure(fig_vol), use_container_width=True)
    with c2:
        st.subheader("Recorded price range")
        st.metric("Lowest recorded price", f'{series["price"].min():,.2f}')
        st.metric("Highest recorded price", f'{series["price"].max():,.2f}')




def load_journal_entries(force: bool = False) -> None:
    """Fetch the signed-in user's persistent journal from the authenticated API."""
    if st.session_state.is_guest:
        return
    user_id = str(st.session_state.user_id)
    if not force and st.session_state.get("journal_loaded_for_user") == user_id:
        return
    try:
        response = requests.get(
            f"{get_api_url()}/api/journal",
            headers=api_headers(),
            timeout=10,
        )
        if response.status_code == 200:
            st.session_state.journal_entries = response.json().get("entries", [])
            st.session_state.journal_loaded_for_user = user_id
        else:
            st.error(f"Could not load journal entries (HTTP {response.status_code}).")
    except requests.RequestException:
        st.error("Journal service is unavailable. Your saved entries have not been changed.")


def clear_journal_entries() -> bool:
    """Clear persistent journal entries for the authenticated user only."""
    if st.session_state.is_guest:
        return False
    try:
        response = requests.delete(
            f"{get_api_url()}/api/journal",
            headers=api_headers(),
            timeout=10,
        )
        if response.status_code == 200:
            st.session_state.journal_entries = []
            st.session_state.journal_loaded_for_user = str(st.session_state.user_id)
            return True
        st.error(f"Could not clear journal entries (HTTP {response.status_code}).")
    except requests.RequestException:
        st.error("Journal service is unavailable. Your saved entries were not cleared.")
    return False


def render_trading_journal(df: pd.DataFrame) -> None:
    st.markdown('<p class="editorial-kicker">Private workspace · Trade notes</p>', unsafe_allow_html=True)
    st.title("Trading journal")
    st.caption("Record the setup, outcome, and decision context behind each trade.")
    if st.session_state.is_guest:
        st.info("Guest demo is read-only for journal persistence. Sign in to save entries across sessions.")
    else:
        load_journal_entries()

    with st.form("journal_entry", clear_on_submit=True):
        st.subheader("New journal entry")
        top1, top2, top3 = st.columns(3)
        with top1:
            trade_date = st.date_input("Trade date", value=datetime.date.today())
            asset = st.text_input("Asset / symbol", placeholder="e.g. NIFTY")
            direction = st.selectbox("Direction", ["Long", "Short"])
        with top2:
            entry_price = st.number_input("Entry price (₹)", min_value=0.0, step=0.05, format="%.2f")
            exit_price = st.number_input("Exit price (₹)", min_value=0.0, step=0.05, format="%.2f")
            strategy = st.text_input("Strategy", placeholder="e.g. Breakout retest")
        with top3:
            pnl_input = st.number_input("Net P&L (₹)", step=0.05, format="%.2f", help="Enter realized P&L after costs. Leave at zero to estimate from price difference, without quantity or fees.")
            confidence = st.slider("Confidence (1–10)", 1, 10, 6)
        notes = st.text_area("Trade notes", placeholder="What was the setup? Did you follow your plan? What would you change next time?", max_chars=2000)
        submitted = st.form_submit_button("Save journal entry", type="primary", use_container_width=True)

    if submitted:
        if st.session_state.is_guest:
            st.warning("Sign in to persist journal entries. Guest mode does not save personal data.")
        elif not asset.strip():
            st.error("Enter an asset or symbol before saving.")
        else:
            computed_pnl = pnl_input
            if pnl_input == 0 and entry_price and exit_price:
                computed_pnl = exit_price - entry_price
                if direction == "Short":
                    computed_pnl = -computed_pnl
            payload = {
                "date": trade_date.isoformat(),
                "asset": asset.strip().upper(),
                "direction": direction,
                "entry": entry_price,
                "exit": exit_price,
                "strategy": strategy.strip(),
                "pnl": computed_pnl,
                "confidence": confidence,
                "notes": notes.strip(),
            }
            try:
                response = requests.post(
                    f"{get_api_url()}/api/journal",
                    json=payload,
                    headers=api_headers(),
                    timeout=10,
                )
                if response.status_code == 201:
                    st.session_state.journal_entries.insert(0, response.json())
                    st.session_state.journal_loaded_for_user = str(st.session_state.user_id)
                    st.success("Journal entry saved to your account.")
                else:
                    st.error(f"Journal entry was not saved (HTTP {response.status_code}). Check your session and API configuration.")
            except requests.RequestException:
                st.error("Journal service is unavailable. The entry was not saved.")

    st.divider()
    st.subheader("Saved entries")
    entries = st.session_state.journal_entries
    if entries:
        table = pd.DataFrame(entries)
        visible = [column for column in ["date", "asset", "direction", "entry", "exit", "pnl", "confidence", "strategy", "notes"] if column in table.columns]
        st.dataframe(table[visible], use_container_width=True, hide_index=True)
        csv = table[visible].to_csv(index=False).encode("utf-8")
        st.download_button("Export journal CSV", data=csv, file_name="trading-journal.csv", mime="text/csv")
        if st.button("Clear all saved entries", type="secondary"):
            if clear_journal_entries():
                st.success("Your journal entries were deleted.")
                st.rerun()
    else:
        st.info("No saved entries yet. Add your first trade above to start building a reviewable history.")

    if not df.empty:
        with st.expander("Imported trade records"):
            visible = [column for column in ["entryAt", "asset", "direction", "pnl", "outcome"] if column in df.columns]
            st.dataframe(df[visible] if visible else df, use_container_width=True, hide_index=True)



def render_portfolio_analytics(df: pd.DataFrame) -> None:
    st.header("Portfolio & Risk Analytics")
    st.caption("Calculations use recorded trade P&L; they are not a complete portfolio valuation.")
    if df.empty:
        st.warning("Add or import trades to calculate analytics.")
        return
    m = calculate_trade_metrics(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net P&L", f'₹{m["total_pnl"]:,.2f}')
    c2.metric("Average P&L / trade", f'₹{m["average_pnl"]:,.2f}')
    c3.metric("Max drawdown", f'₹{m["max_drawdown"]:,.2f}')
    factor = m["profit_factor"]
    c4.metric("Profit factor", "∞" if factor == float("inf") else "N/A" if factor is None else f"{factor:.2f}x")
    st.divider()
    left, right = st.columns(2, gap="large")
    normalized = normalize_trades(df)
    with left:
        st.subheader("Trade count by asset")
        if "asset" in normalized.columns:
            counts = normalized["asset"].fillna("Unknown").value_counts().rename_axis("Asset").reset_index(name="Trades")
            fig = px.bar(counts, x="Asset", y="Trades", template="plotly_white")
            st.plotly_chart(style_figure(fig), use_container_width=True)
        else:
            st.info("Asset names are not available in these records.")
    with right:
        st.subheader("Net P&L by asset")
        if "asset" in normalized.columns:
            by_asset = normalized.groupby("asset", dropna=False)["pnl"].sum().sort_values().rename_axis("Asset").reset_index(name="Net P&L")
            fig = px.bar(by_asset, x="Net P&L", y="Asset", orientation="h", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Asset names are not available in these records.")
    st.subheader("Behavioral data quality")
    available = [name for name in ["confidence", "emotion_score", "emotionScore", "strategy"] if name in normalized.columns]
    if available:
        st.write("Recorded fields available for future behavioral analysis: " + ", ".join(available))
        st.caption("No discipline or emotional-control score is fabricated when supporting observations are absent.")
    else:
        st.info("No confidence, emotion, or strategy fields are available. Record these fields before calculating behavioral scores.")



@st.cache_resource
def load_ml_models():
    try:
        model = joblib.load(MODEL_DIR / "trade_predictor.joblib")
        scaler = joblib.load(MODEL_DIR / "scaler.joblib")
        return model, scaler
    except Exception as e:
        return None, None

def render_trade_predictions() -> None:
    st.header("Trade Prediction Sandbox")
    st.warning("Research/demo model: the training pipeline generates synthetic outcomes. Scores are not validated on real trading data and must not be used as financial advice.")
    model, scaler = load_ml_models()
    if model is None or scaler is None:
        st.error("The model or scaler is unavailable. Run frontend-streamlit/training/train_model.py and refresh.")
        return
    features = ["hour_of_day", "volume_normalized", "risk_reward_ratio", "volatility_index", "emotion_score", "trend_strength"]
    left, right = st.columns([1, 1.5], gap="large")
    with left:
        st.subheader("Input features")
        with st.form("prediction_form"):
            hour = st.slider("Hour of day", 9, 15, 10)
            volume = st.slider("Normalized volume", 0.5, 2.5, 1.2)
            risk_reward = st.slider("Risk/reward ratio", 0.5, 3.5, 2.0)
            volatility = st.slider("Volatility index (synthetic scale)", 10.0, 40.0, 20.0)
            emotion = st.slider("Emotion score (higher = more intense)", 1, 99, 30)
            trend = st.slider("Trend strength", -1.0, 1.0, 0.5)
            submitted = st.form_submit_button("Evaluate sample", type="primary", use_container_width=True)
        if submitted:
            st.session_state.last_prediction_input = [hour, volume, risk_reward, volatility, emotion, trend]
    with right:
        st.subheader("Model output")
        if "last_prediction_input" not in st.session_state:
            st.info("Choose feature values and select Evaluate sample to inspect the model output.")
            return
        try:
            input_df = pd.DataFrame([st.session_state.last_prediction_input], columns=features)
            scaled = scaler.transform(input_df)
            probability = float(model.predict_proba(scaled)[0][1])
            st.metric("Model-estimated class-1 probability", f"{probability:.1%}")
            st.progress(max(0.0, min(1.0, probability)))
            st.caption("A model score on synthetic training data—not a real-world win probability.")
            st.divider()
            st.subheader("SHAP feature contributions")
            try:
                explainer = shap.TreeExplainer(model)
                explanation = explainer(scaled)
                values = np.asarray(explanation.values)
                if values.ndim == 3:
                    values = values[:, :, 1]
                contributions = values[0]
                ranking = sorted(zip(features, contributions), key=lambda item: abs(float(item[1])), reverse=True)
                chart_df = pd.DataFrame({"Feature": [item[0].replace("_", " ").title() for item in ranking], "Contribution": [float(item[1]) for item in ranking]})
                fig = px.bar(chart_df, x="Contribution", y="Feature", orientation="h", color="Contribution", color_continuous_midpoint=0, template="plotly_white")
                fig.update_layout(height=320, margin=dict(l=8, r=8, t=16, b=8), coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                st.caption("SHAP is unavailable for this model/runtime combination. No explanation has been fabricated.")
        except Exception:
            st.error("Prediction failed: the model and scaler may not match the expected feature schema. Retrain both artifacts together.")




def render_settings() -> None:
    st.header("Settings")
    
    if st.session_state.is_guest:
        st.warning("Backend account management and export are not implemented in this prototype. Use guest mode for the safe demo experience.")
        return

    st.text_input("API URL", key="api_url")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Refresh Trades"):
            load_user_trades(force=True)
            st.success("Trades refreshed.")
    with col2:
        if st.button("Clear Chat"):
            st.session_state.coach_messages = []
            st.success("Chat cleared.")
    with col3:
        if st.button("Clear Journal"):
            if clear_journal_entries():
                st.success("Journal cleared.")

    st.subheader("Behavioral Profiling")
    if st.button("Run Profiling"):
        with st.spinner("Analyzing behavior..."):
            try:
                resp = requests.get(
                    f"{get_api_url()}/api/profiling/{st.session_state.user_id}",
                    headers=api_headers(), timeout=10,
                )
                if resp.status_code == 200:
                    profile = resp.json()
                    st.success("Profiling complete.")
                    st.write(
                        profile.get("behavior", "Unknown").replace("_", " ").title()
                    )
                    st.write(profile.get("summary", "No summary provided."))
                else:
                    st.error("Failed to fetch profiling data.")
            except requests.RequestException:
                st.error("Profiling request failed. Check the API service and try again.")


init_session_state()
apply_editorial_theme()

if not st.session_state.welcome_screen_passed:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=68)
    st.markdown('<p class="editorial-kicker">ATC / Trading intelligence</p>', unsafe_allow_html=True)
    st.title("Read the market.\nKnow your edge.")
    st.markdown("A thoughtful workspace for reviewing recorded performance, risk, and trading decisions.")
    st.caption("DEMO WORKSPACE · Illustrative trades only · No live market feed connected")
    st.divider()

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown('<div class="editorial-panel">', unsafe_allow_html=True)
        st.subheader("A clearer view of your trading.")
        st.write("Track historical trade outcomes, review price records, and capture the context behind your decisions.")
        st.markdown("- Historical performance metrics")
        st.markdown("- Explainable synthetic-model sandbox")
        st.markdown("- Private journal for authenticated users")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Explore the demo", use_container_width=True, type="primary"):
            st.session_state.welcome_screen_passed = True
            st.session_state.is_guest = True
            st.rerun()
    with right:
        st.markdown('<div class="editorial-panel">', unsafe_allow_html=True)
        st.subheader("Sign in to your workspace")
        st.caption("Authentication requires a configured API user and strong JWT secret.")
        with st.form("welcome_login_form"):
            user_id_input = st.text_input("User ID", placeholder="Your configured user ID")
            password_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
            if submitted:
                if user_id_input.strip():
                    login(user_id_input.strip(), password_input)
                else:
                    st.error("Enter your user ID to continue.")
        st.markdown('</div>', unsafe_allow_html=True)


    st.stop()

# Sidebar Authentication
st.sidebar.image(str(LOGO_PATH), width=50)
st.sidebar.markdown("<p class=\"editorial-kicker\">ATC / Research desk</p>", unsafe_allow_html=True)
st.sidebar.title("Trading Coach")
st.sidebar.caption("Trade history · Risk · Review")
st.sidebar.divider()

if st.session_state.is_guest:
    st.sidebar.markdown("**DEMO WORKSPACE**")
    st.sidebar.caption("Sample portfolio · Read-only journal")
    with st.sidebar.expander("Sign in"):
        st.caption("Sign-in is available when the API is configured with a user password hash and strong JWT secret.")
        with st.form("sidebar_login_form"):
            user_id_input = st.text_input("Username (User ID)")
            password_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted and user_id_input:
                login(user_id_input, password_input)
else:
    display_id = str(st.session_state.user_id)
    st.sidebar.markdown(f"👤 **{display_id}**")
    st.sidebar.caption("Authenticated workspace")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_id = "guest_demo"
        st.session_state.is_guest = True
        st.session_state.trades_data = []
        st.session_state.journal_entries = []
        st.session_state.pop("journal_loaded_for_user", None)
        st.session_state.coach_messages = []
        st.session_state.discipline_score = None
        st.rerun()

st.sidebar.divider()

# Main Application
load_user_trades()
df_trades = build_trade_frame(st.session_state.trades_data)

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "AI Coach",
        "Market Analysis",
        "Trade Predictions",
        "Trading Journal",
        "Portfolio Analytics",
        "Settings",
    ],
)

if page == "Dashboard":
    render_dashboard(df_trades)
elif page == "AI Coach":
    render_ai_coach(df_trades)
elif page == "Market Analysis":
    render_market_analysis(df_trades)
elif page == "Trade Predictions":
    render_trade_predictions()
elif page == "Trading Journal":
    render_trading_journal(df_trades)
elif page == "Portfolio Analytics":
    render_portfolio_analytics(df_trades)
elif page == "Settings":
    render_settings()
