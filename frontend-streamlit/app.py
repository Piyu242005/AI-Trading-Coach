import datetime
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

DEFAULT_API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Trading Coach", page_icon="📈", layout="wide")


def init_session_state() -> None:
    defaults = {
        "token": None,
        "user_id": None,
        "trades_data": [],
        "journal_entries": [],
        "coach_messages": [],
        "api_url": DEFAULT_API_URL,
        "discipline_score": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_api_url() -> str:
    return str(st.session_state.api_url).rstrip("/")


def api_headers() -> Dict[str, str]:
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login(user_id: str, password: str) -> None:
    try:
        response = requests.post(
            f"{get_api_url()}/api/auth/token", json={"userId": user_id}
        )
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.session_state.user_id = user_id
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Authentication failed. Check your User ID.")
    except Exception as exc:
        st.error(f"Failed to connect to backend: {exc}")


def load_user_trades(force: bool = False) -> None:
    if st.session_state.trades_data and not force:
        return

    try:
        response = requests.get(f"{get_api_url()}/api/trades")
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
    except Exception as exc:
        st.error(f"Error loading trades: {exc}")


def fetch_discipline_score() -> Optional[Dict[str, str]]:
    try:
        response = requests.get(
            f"{get_api_url()}/api/discipline-score/{st.session_state.user_id}",
            headers=api_headers(),
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


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
        df["outcome"] = df["pnl"].apply(lambda value: "win" if value >= 0 else "loss")
    return df


def compute_summary_metrics(df: pd.DataFrame) -> Dict[str, object]:
    total_trades = len(df)
    wins = len(df[df["outcome"] == "win"]) if "outcome" in df.columns else 0
    win_rate = (wins / total_trades * 100) if total_trades else 0
    total_pnl = df["pnl"].sum() if "pnl" in df.columns else 0
    portfolio_value = 100000 + total_pnl

    last_trade_date = None
    if "entryAt" in df.columns and not df["entryAt"].dropna().empty:
        last_trade_date = df["entryAt"].dropna().max()

    if last_trade_date is not None and not pd.isna(last_trade_date):
        todays_pnl = df.loc[
            df["entryAt"].dt.date == last_trade_date.date(), "pnl"
        ].sum()
    else:
        todays_pnl = 0

    if win_rate >= 60:
        sentiment = "Bullish"
    elif win_rate <= 40:
        sentiment = "Bearish"
    else:
        sentiment = "Neutral"

    return {
        "total_trades": total_trades,
        "wins": wins,
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "portfolio_value": portfolio_value,
        "todays_pnl": todays_pnl,
        "sentiment": sentiment,
    }


def build_price_series(df: pd.DataFrame, asset: str) -> pd.DataFrame:
    asset_df = df.copy()
    if "asset" in asset_df.columns:
        asset_df = asset_df[asset_df["asset"] == asset]
    asset_df = asset_df.sort_values("entryAt") if "entryAt" in asset_df.columns else asset_df

    if not asset_df.empty and "entryAt" in asset_df.columns:
        asset_df = asset_df.dropna(subset=["entryAt"]) if "entryAt" in asset_df.columns else asset_df
        price_source = None
        if "entryPrice" in asset_df.columns and asset_df["entryPrice"].sum() != 0:
            price_source = "entryPrice"
        elif "exitPrice" in asset_df.columns and asset_df["exitPrice"].sum() != 0:
            price_source = "exitPrice"

        if price_source:
            series = asset_df[["entryAt", price_source]].rename(
                columns={"entryAt": "date", price_source: "price"}
            )
            return series

    end_date = datetime.date.today()
    dates = [end_date - datetime.timedelta(days=idx) for idx in range(59, -1, -1)]
    price = [100 + idx * 0.35 + ((idx % 10) - 5) * 0.4 for idx in range(60)]
    return pd.DataFrame({"date": dates, "price": price})


def render_dashboard(df: pd.DataFrame) -> None:
    st.header("Dashboard")
    metrics = compute_summary_metrics(df)

    discipline = st.session_state.discipline_score
    if discipline is None:
        discipline = fetch_discipline_score()
        st.session_state.discipline_score = discipline

    risk_score = discipline.get("score") if discipline else None
    risk_level = discipline.get("risk_level") if discipline else "Unknown"

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Portfolio Value", f"${metrics['portfolio_value']:,.0f}")
    col2.metric("Today's P/L", f"${metrics['todays_pnl']:.2f}")
    if risk_score is not None:
        col3.metric("Risk Score", f"{risk_score}/100")
    else:
        col3.metric("Risk Score", "--")
    col4.metric("Market Sentiment", metrics["sentiment"])
    col5.metric("Top Opportunities", "3 ideas")

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Equity Curve")
        if not df.empty and "entryAt" in df.columns:
            df_sorted = df.sort_values("entryAt")
            df_sorted["cumulative_pnl"] = df_sorted["pnl"].cumsum()
            fig = px.line(
                df_sorted,
                x="entryAt",
                y="cumulative_pnl",
                labels={"entryAt": "Date", "cumulative_pnl": "Cumulative P&L ($)"},
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trade history yet.")

    with col_right:
        st.subheader("Top Opportunities")
        if not df.empty and "asset" in df.columns:
            opportunity_df = (
                df.groupby("asset")["pnl"].mean().sort_values(ascending=False)
            )
            top_assets = opportunity_df.head(3)
            for asset, score in top_assets.items():
                st.markdown(f"- **{asset}** avg P&L: ${score:.2f}")
        else:
            st.markdown("- BTC: momentum setup\n- AAPL: breakout watch\n- ETH: mean reversion")

        st.subheader("Risk Snapshot")
        st.write(f"Risk Level: {risk_level}")
        if discipline:
            st.write(
                "Confidence:", f"{discipline.get('confidence', 0)}%",
            )

    if not df.empty:
        st.subheader("Win/Loss Distribution")
        if "assetClass" in df.columns:
            group_col = "assetClass"
        elif "asset" in df.columns:
            group_col = "asset"
        else:
            group_col = None

        if group_col:
            fig2 = px.histogram(
                df,
                x=group_col,
                color="outcome",
                barmode="group",
                template="plotly_dark",
            )
            st.plotly_chart(fig2, use_container_width=True)

    with st.expander("Raw Trades"):
        if not df.empty:
            cols = [
                col
                for col in [
                    "tradeId",
                    "asset",
                    "direction",
                    "entryPrice",
                    "exitPrice",
                    "pnl",
                    "outcome",
                ]
                if col in df.columns
            ]
            st.dataframe(df[cols])
        else:
            st.write("No trades available.")


def render_ai_coach(df: pd.DataFrame) -> None:
    st.header("AI Coach Chat")
    st.markdown("Ask questions and get feedback grounded in your recent trades.")

    if not st.session_state.coach_messages:
        st.session_state.coach_messages.append(
            {"role": "assistant", "content": "Ask me about your trades."}
        )

    for message in st.session_state.coach_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask Trading Coach...")
    if prompt:
        st.session_state.coach_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        if df.empty:
            reply = "I do not have trades to analyze yet. Load your trades first."
            st.session_state.coach_messages.append(
                {"role": "assistant", "content": reply}
            )
            with st.chat_message("assistant"):
                st.write(reply)
            return

        with st.chat_message("assistant"):
            with st.spinner("Reviewing your recent trades..."):
                payload = {"trades": st.session_state.trades_data[-20:]}
                try:
                    resp = requests.post(
                        f"{get_api_url()}/api/coaching/{st.session_state.user_id}",
                        json=payload,
                        headers=api_headers(),
                    )
                    if resp.status_code == 200:
                        coaching = resp.json()
                        message = coaching.get("message", "")
                        signals = coaching.get("signals", [])
                        response_lines = [message]
                        if signals:
                            response_lines.append("\nSignals:")
                            for signal in signals:
                                response_lines.append(
                                    f"- {signal['signal'].replace('_', ' ').title()}: {signal['reason']}"
                                )
                        reply = "\n".join(response_lines)
                    else:
                        reply = "I could not reach the coaching engine. Try again."
                    st.write(reply)
                    st.session_state.coach_messages.append(
                        {"role": "assistant", "content": reply}
                    )
                except Exception as exc:
                    reply = f"Backend error: {exc}"
                    st.write(reply)
                    st.session_state.coach_messages.append(
                        {"role": "assistant", "content": reply}
                    )


def render_market_analysis(df: pd.DataFrame) -> None:
    st.header("Market Analysis")
    st.markdown("Explore trends, indicators, and volatility for your watchlist.")

    if not df.empty and "asset" in df.columns:
        assets = sorted({asset for asset in df["asset"].dropna().unique()})
    else:
        assets = ["AAPL", "TSLA", "BTC", "ETH", "NIFTY"]

    selected_asset = st.selectbox("Asset", assets)
    series = build_price_series(df, selected_asset)

    series["ma"] = series["price"].rolling(window=5).mean()
    series["returns"] = series["price"].pct_change().fillna(0)
    series["volatility"] = series["returns"].rolling(window=5).std().fillna(0) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series["date"], y=series["price"], name="Price"))
    fig.add_trace(
        go.Scatter(x=series["date"], y=series["ma"], name="5D MA")
    )
    fig.update_layout(template="plotly_dark", height=380)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Volatility")
        vol_fig = px.area(
            series,
            x="date",
            y="volatility",
            labels={"volatility": "Volatility (%)"},
            template="plotly_dark",
        )
        st.plotly_chart(vol_fig, use_container_width=True)

    with col2:
        st.subheader("Support / Resistance")
        support = series["price"].quantile(0.25)
        resistance = series["price"].quantile(0.75)
        st.metric("Support", f"{support:.2f}")
        st.metric("Resistance", f"{resistance:.2f}")
        st.write("Signals: trend-follow + mean reversion zones")


def render_trading_journal(df: pd.DataFrame) -> None:
    st.header("Trading Journal")
    st.markdown("Log trades, strategies, and notes for review.")

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
    st.header("Portfolio Analytics")
    st.markdown("Allocation, risk, and performance analytics.")

    discipline = st.session_state.discipline_score
    if discipline is None:
        discipline = fetch_discipline_score()
        st.session_state.discipline_score = discipline

    if df.empty:
        st.info("Load trades to see portfolio analytics.")
        return

    group_col = "assetClass" if "assetClass" in df.columns else "asset"
    allocation = df.groupby(group_col).size().reset_index(name="trades")
    allocation_fig = px.pie(
        allocation,
        names=group_col,
        values="trades",
        template="plotly_dark",
        title="Asset Allocation",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(allocation_fig, use_container_width=True)
    with col2:
        daily_pnl = df.copy()
        if "entryAt" in daily_pnl.columns:
            daily_pnl = (
                daily_pnl.dropna(subset=["entryAt"])
                .groupby(daily_pnl["entryAt"].dt.date)["pnl"]
                .sum()
            )
        else:
            daily_pnl = pd.Series([0])

        returns = daily_pnl / 100000
        if returns.std() and len(returns) > 1:
            sharpe = (returns.mean() / returns.std()) * (252**0.5)
        else:
            sharpe = 0

        if "entryAt" in df.columns:
            cumulative = df.sort_values("entryAt")["pnl"].cumsum()
        else:
            cumulative = df["pnl"].cumsum()
        running_max = cumulative.cummax()
        drawdown = cumulative - running_max
        max_drawdown = drawdown.min() if not drawdown.empty else 0

        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        st.metric("Max Drawdown", f"${max_drawdown:.2f}")
        if discipline:
            st.metric("Risk Level", discipline.get("risk_level", "--"))

    st.subheader("Risk Analysis")
    if discipline:
        st.write(
            f"Discipline Score: {discipline.get('score')}/100 | Confidence: {discipline.get('confidence')}%"
        )
        st.write("Drivers:", discipline.get("contributors", {}))
    else:
        st.write("Risk model unavailable. Check API connectivity.")


def render_settings() -> None:
    st.header("Settings")
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
                    headers=api_headers(),
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
            except Exception as exc:
                st.error(f"Profiling error: {exc}")


init_session_state()

# Sidebar Authentication
st.sidebar.title("🔐 Login")
if not st.session_state.token:
    with st.sidebar.form("login_form"):
        st.markdown("**Test User ID:** `Piyu24`")
        user_id_input = st.text_input("Username (User ID)")
        password_input = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted and user_id_input:
            login(user_id_input, password_input)
else:
    display_id = str(st.session_state.user_id)
    st.sidebar.success(f"Logged in as: {display_id[:8]}...")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_id = None
        st.session_state.trades_data = []
        st.session_state.discipline_score = None
        st.rerun()

# Main Application
if st.session_state.token:
    load_user_trades()
    df_trades = build_trade_frame(st.session_state.trades_data)

    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigate",
        [
            "Dashboard",
            "AI Coach",
            "Market Analysis",
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
    elif page == "Trading Journal":
        render_trading_journal(df_trades)
    elif page == "Portfolio Analytics":
        render_portfolio_analytics(df_trades)
    elif page == "Settings":
        render_settings()
else:
    st.title("AI Trading Coach")
    st.info("Please login using the sidebar to view your Trading Dashboard.")
