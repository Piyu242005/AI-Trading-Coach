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

st.set_page_config(page_title="AI Trading Coach", page_icon="📈", layout="wide")

def apply_dark_theme() -> None:
    """Apply the warm, editorial design system across the Streamlit application."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

        :root {
          color-scheme: light;
          --paper: #f7f4ed;
          --surface: #fffdf8;
          --ink: #202a25;
          --muted: #6d766e;
          --line: #e5dfd2;
          --forest: #233d32;
          --sage: #718875;
          --rust: #c65c3d;
          --gold: #d9ad60;
        }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp { background: var(--paper); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(247,244,237,.94); }
        [data-testid="stMainBlockContainer"] { max-width: 1440px; padding-top: 2.2rem; padding-bottom: 4rem; }
        h1, h2, h3, [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
          color: var(--ink); font-family: 'Playfair Display', Georgia, serif;
          letter-spacing: -.035em; line-height: 1.12;
        }
        h1 { font-size: clamp(2.2rem, 4vw, 3.5rem) !important; }
        h2 { font-size: clamp(1.6rem, 2.7vw, 2.2rem) !important; }
        h3 { font-size: 1.35rem !important; }
        p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }
        [data-testid="stSidebar"] {
          background: var(--forest); border-right: 0; box-shadow: 8px 0 30px rgba(32,42,37,.05);
        }
        [data-testid="stSidebar"] * { color: #f8f5ed; }
        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.16); }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
          color: #fffaf0; font-family: 'DM Sans', sans-serif; letter-spacing: -.02em;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label { color: #e7e9df; }
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { color: #f0c58a; }
        [data-testid="stMetric"] {
          background: var(--surface); border: 1px solid var(--line); border-radius: 5px;
          padding: 1.15rem 1.25rem; box-shadow: 0 5px 18px rgba(46,47,35,.025);
        }
        [data-testid="stMetricLabel"] { color: var(--muted); font-size: .82rem; font-weight: 600; }
        [data-testid="stMetricValue"] { color: var(--ink); font-family: 'Playfair Display', Georgia, serif; font-size: clamp(1.5rem,2vw,2rem); }
        [data-testid="stMetricDelta"] { font-size: .8rem; }
        .stButton > button, .stFormSubmitButton > button {
          border-radius: 4px; border: 1px solid var(--forest); min-height: 2.8rem;
          font-weight: 700; letter-spacing: .01em; transition: transform .16s ease, box-shadow .16s ease;
        }
        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
          background: var(--rust); border-color: var(--rust); color: #fffdf8;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
          transform: translateY(-1px); box-shadow: 0 7px 18px rgba(32,42,37,.10); border-color: var(--rust);
        }
        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] {
          background: var(--surface); border-color: var(--line); border-radius: 4px;
        }
        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"], [data-testid="stTable"] {
          background: var(--surface); border: 1px solid var(--line); border-radius: 5px; overflow: hidden;
        }
        [data-testid="stAlert"] { border-radius: 4px; }
        hr { border-color: var(--line); }
        .editorial-kicker {
          color: var(--rust); font-size: .72rem; font-weight: 700; letter-spacing: .18em;
          text-transform: uppercase; margin: 0 0 .65rem 0;
        }
        .editorial-hero {
          background: var(--forest); color: #f8f5ed; padding: clamp(1.5rem,4vw,3.3rem);
          border-radius: 5px; margin: 0 0 1.5rem 0; position: relative; overflow: hidden;
        }
        .editorial-hero:after {
          content: ''; position: absolute; width: 240px; height: 240px; border: 1px solid rgba(240,197,138,.25);
          border-radius: 50%; right: -85px; top: -100px; box-shadow: 0 0 0 28px rgba(240,197,138,.035), 0 0 0 58px rgba(240,197,138,.025);
        }
        .editorial-hero .editorial-kicker { color: #efbd80; }
        .editorial-hero h1 { color: #fffaf0; max-width: 760px; margin: 0; font-size: clamp(2.3rem,5vw,4.4rem) !important; }
        .editorial-hero p { color: #d4ddd3; max-width: 680px; font-size: 1.02rem; line-height: 1.75; margin: 1rem 0 0; }
        .editorial-rule { border-top: 1px solid var(--line); margin: 1.4rem 0; }
        .editorial-note { color: var(--muted); font-size: .86rem; line-height: 1.65; }
        @media (max-width: 768px) {
          [data-testid="stMainBlockContainer"] { padding: 1.1rem 1rem 2.5rem; }
          [data-testid="stMetric"] { padding: .8rem; }
          .editorial-hero { padding: 1.5rem; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



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
    st.markdown(
        """
        <section class="editorial-hero">
          <div class="editorial-kicker">The trading journal · Issue 01</div>
          <h1>Clarity over noise.</h1>
          <p>A considered view of your trade history: performance, risk and patterns in one calm workspace. Numbers below describe recorded trades—not future outcomes.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.is_guest:
        st.caption("DEMO EDITION  /  The sample portfolio is illustrative. It is not live market data or your personal trading history.")
    if df.empty:
        st.warning("No trade records are available yet. Add or import trades to begin your performance review.")
        return

    metrics = calculate_trade_metrics(df)
    factor = metrics["profit_factor"]
    factor_label = "∞" if factor == float("inf") else "—" if factor is None else f'{factor:.2f}x'
    total_pnl = metrics["total_pnl"]
    prefix = "+" if total_pnl > 0 else ""
    cards = st.columns(5)
    cards[0].metric("RECORDED TRADES", f'{metrics["total_trades"]:,}')
    cards[1].metric("HISTORICAL WIN RATE", f'{metrics["win_rate"]:.1f}%')
    cards[2].metric("NET P&L", f'{prefix}${total_pnl:,.2f}')
    cards[3].metric("PROFIT FACTOR", factor_label)
    cards[4].metric("MAX DRAWDOWN", f'${metrics["max_drawdown"]:,.2f}')

    st.markdown('<div class="editorial-rule"></div>', unsafe_allow_html=True)
    col_heading, col_context = st.columns([1.4, 1])
    with col_heading:
        st.markdown('<div class="editorial-kicker">01 / Performance</div>', unsafe_allow_html=True)
        st.subheader("The shape of your results")
    with col_context:
        st.markdown('<p class="editorial-note">Cumulative profit and loss helps show the sequence behind the final result. A positive total alone does not describe risk.</p>', unsafe_allow_html=True)
    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.markdown("**Cumulative P&L**")
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
            fig.update_traces(line=dict(color="#c65c3d", width=3), fill="tozeroy", fillcolor="rgba(198,92,61,0.08)")
            fig.update_layout(
                margin=dict(l=16, r=16, t=18, b=12), height=330,
                xaxis_title="", yaxis_title="P&L", paper_bgcolor="#fffdf8", plot_bgcolor="#fffdf8",
                font=dict(family="DM Sans, sans-serif", color="#202a25"),
                xaxis=dict(showgrid=False, linecolor="#e5dfd2"),
                yaxis=dict(gridcolor="#eee8dd", zerolinecolor="#c9c0b1"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        else:
            st.caption("Add valid trade dates to reveal the cumulative P&L timeline.")
    with right:
        st.markdown("**Trade outcomes**")
        counts = normalize_trades(df)["outcome"].value_counts().rename_axis("Outcome").reset_index(name="Trades")
        fig = px.pie(counts, names="Outcome", values="Trades", hole=0.68, template="plotly_white",
                     color="Outcome", color_discrete_map={"win": "#718875", "loss": "#c65c3d", "breakeven": "#d9ad60", "unknown": "#a8aaa1"})
        fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#fffdf8", width=3)))
        fig.update_layout(
            margin=dict(l=8, r=8, t=18, b=8), height=330, legend_title_text="",
            paper_bgcolor="#fffdf8", plot_bgcolor="#fffdf8",
            font=dict(family="DM Sans, sans-serif", color="#202a25"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.caption(f'{metrics["wins"]} wins  ·  {metrics["losses"]} losses  ·  {metrics["breakeven"]} breakeven')

    st.markdown('<div class="editorial-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="editorial-kicker">02 / Ledger</div>', unsafe_allow_html=True)
    st.subheader("Trade-by-trade")
    st.markdown('<p class="editorial-note">A clean ledger of the records currently available to this session.</p>', unsafe_allow_html=True)
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
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=12, r=12, t=24, b=12), xaxis_title="Recorded date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Rolling average and volatility describe the available trade-price records; they are not live technical signals.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Observed price variation")
        fig_vol = px.area(series, x="date", y="volatility", labels={"volatility": "Rolling variation (%)"}, template="plotly_dark")
        st.plotly_chart(fig_vol, use_container_width=True)
    with c2:
        st.subheader("Recorded price range")
        st.metric("Lowest recorded price", f'{series["price"].min():,.2f}')
        st.metric("Highest recorded price", f'{series["price"].max():,.2f}')




def render_trading_journal(df: pd.DataFrame) -> None:
    st.header("Trading Journal")
    st.markdown("Log trades, strategies, and notes for review.")
    st.caption("Journal entries are stored in the current Streamlit session only; persistent journal storage is not connected yet.")

    with st.form("journal_entry"):
        col1, col2, col3 = st.columns(3)
        with col1:
            trade_date = st.date_input("Date", value=datetime.date.today())
            asset = st.text_input("Asset")
            direction = st.selectbox("Direction", ["Long", "Short"])
        with col2:
            entry_price = st.number_input("Entry Price", min_value=0.0, step=0.01)
            exit_price = st.number_input("Exit Price", min_value=0.0, step=0.01)
            strategy = st.text_input("Strategy")
        with col3:
            pnl = st.number_input("P&L", step=0.01)
            confidence = st.slider("Confidence", 1, 10, 6)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add to Journal")

        if submitted and asset:
            if st.session_state.is_guest:
                st.warning("🔒 Login Required: Sign in to save your progress and unlock full platform features.")
            else:
                computed_pnl = pnl
                if pnl == 0 and entry_price and exit_price:
                    computed_pnl = exit_price - entry_price
                    if direction == "Short":
                        computed_pnl = -computed_pnl

                st.session_state.journal_entries.append(
                    {
                        "date": trade_date.isoformat(),
                        "asset": asset,
                        "direction": direction,
                        "entry": entry_price,
                        "exit": exit_price,
                        "strategy": strategy,
                        "pnl": computed_pnl,
                        "confidence": confidence,
                        "notes": notes,
                    }
                )
                st.success("Entry added.")

    if st.session_state.journal_entries:
        st.subheader("Journal Entries")
        st.dataframe(pd.DataFrame(st.session_state.journal_entries))

    if not df.empty:
        st.subheader("Imported Trades")
        st.dataframe(df[[col for col in df.columns if col in ["entryAt", "asset", "direction", "pnl"]]])


def render_portfolio_analytics(df: pd.DataFrame) -> None:
    st.header("Portfolio & Risk Analytics")
    st.caption("Calculations use recorded trade P&L; they are not a complete portfolio valuation.")
    if df.empty:
        st.warning("Add or import trades to calculate analytics.")
        return
    m = calculate_trade_metrics(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net P&L", f'${m["total_pnl"]:,.2f}')
    c2.metric("Average P&L / trade", f'${m["average_pnl"]:,.2f}')
    c3.metric("Max drawdown", f'${m["max_drawdown"]:,.2f}')
    factor = m["profit_factor"]
    c4.metric("Profit factor", "∞" if factor == float("inf") else "N/A" if factor is None else f"{factor:.2f}x")
    st.divider()
    left, right = st.columns(2, gap="large")
    normalized = normalize_trades(df)
    with left:
        st.subheader("Trade count by asset")
        if "asset" in normalized.columns:
            counts = normalized["asset"].fillna("Unknown").value_counts().rename_axis("Asset").reset_index(name="Trades")
            fig = px.bar(counts, x="Asset", y="Trades", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Asset names are not available in these records.")
    with right:
        st.subheader("Net P&L by asset")
        if "asset" in normalized.columns:
            by_asset = normalized.groupby("asset", dropna=False)["pnl"].sum().sort_values().rename_axis("Asset").reset_index(name="Net P&L")
            fig = px.bar(by_asset, x="Net P&L", y="Asset", orientation="h", template="plotly_dark")
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
                fig = px.bar(chart_df, x="Contribution", y="Feature", orientation="h", color="Contribution", color_continuous_midpoint=0, template="plotly_dark")
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
            st.session_state.journal_entries = []
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
apply_dark_theme()

if not st.session_state.welcome_screen_passed:
    st.markdown(
        """
        <section class="editorial-hero">
          <div class="editorial-kicker">A more thoughtful trading workspace</div>
          <h1>Read the market.<br>Understand yourself.</h1>
          <p>Trade-history analytics, explainable model experiments and a quieter way to review performance—designed to put context before impulse.</p>
        </section>
        <div class="editorial-kicker">Start here / Choose your edition</div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("### Explore the demo")
        st.markdown("An instant, read-only-feeling tour using clearly labeled illustrative trades. Explore performance metrics, outcome charts and portfolio summaries without configuring an account.")
        if st.button("Explore guest edition  →", use_container_width=True, type="primary"):
            st.session_state.welcome_screen_passed = True
            st.session_state.is_guest = True
            st.rerun()
    with col2:
        st.markdown("### Sign in to your workspace")
        st.markdown("Connect to your configured backend to inspect your account's recorded trades. Authentication must be configured on the API host before sign-in can succeed.")
        with st.expander("Open sign-in"):
            with st.form("welcome_login_form"):
                user_id_input = st.text_input("User ID")
                password_input = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
                if submitted and user_id_input and password_input:
                    login(user_id_input, password_input)
    st.markdown('<div class="editorial-rule"></div><p class="editorial-note">FIELD NOTE 01 — This is an educational portfolio prototype. Model scores are trained on synthetic data; this is not financial advice.</p>', unsafe_allow_html=True)


    st.stop()

# Sidebar Authentication
st.sidebar.image(str(LOGO_PATH), width=50)
st.sidebar.markdown("### AI Trading Coach")
st.sidebar.markdown("*Trade intelligence · Field notes*")
st.sidebar.markdown("---")

if st.session_state.is_guest:
    st.sidebar.markdown("**GUEST EDITION**")
    st.sidebar.markdown("Illustrative sample portfolio")
    with st.sidebar.expander("Login for Full Access"):
        st.caption("Password verification requires AI_TRADING_COACH_USERS_JSON and a strong JWT_SECRET on the backend. Use Guest demo if credentials are not configured.")
        with st.form("sidebar_login_form"):
            user_id_input = st.text_input("Username (User ID)")
            password_input = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted and user_id_input:
                login(user_id_input)
else:
    display_id = str(st.session_state.user_id)
    st.sidebar.markdown(f"👤 **{display_id}**")
    st.sidebar.markdown("Portfolio Owner")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_id = "guest_demo"
        st.session_state.is_guest = True
        st.session_state.trades_data = []
        st.session_state.journal_entries = []
        st.session_state.coach_messages = []
        st.session_state.discipline_score = None
        st.rerun()

st.sidebar.markdown("━━━━━━━━━━━━━━━")

# Main Application
load_user_trades()
df_trades = build_trade_frame(st.session_state.trades_data)

page = st.sidebar.radio(
    "Navigate",
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
