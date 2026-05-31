import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Trading Coach", page_icon="📈", layout="wide")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "trades_data" not in st.session_state:
    st.session_state.trades_data = []


def login(user_id, password):
    # In a real app, we'd verify the password here.
    # For now, we request a token for the user_id.
    try:
        response = requests.post(f"{API_URL}/api/auth/token", json={"userId": user_id})
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.session_state.user_id = user_id
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Authentication failed. Check your User ID.")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")


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
    st.sidebar.success(f"Logged in as: {st.session_state.user_id[:8]}...")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_id = None
        st.rerun()

# Main Application
if st.session_state.token:
    st.title("📈 AI Trading Coach Dashboard")

    # Fetch user data
    def load_user_trades():
        try:
            response = requests.get(f"{API_URL}/api/trades")
            if response.status_code == 200:
                data = response.json()
                traders = data.get("traders", [])

                # Find current user's trades
                all_trades = []
                for trader in traders:
                    if trader["userId"] == st.session_state.user_id:
                        for session in trader.get("sessions", []):
                            all_trades.extend(session.get("trades", []))

                st.session_state.trades_data = all_trades
        except Exception as e:
            st.error(f"Error loading trades: {e}")

    load_user_trades()

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 AI Profiling", "🤖 AI Coach"])

    with tab1:
        st.header("Portfolio Analytics")
        trades = st.session_state.trades_data

        if trades:
            df = pd.DataFrame(trades)
            df["entryAt"] = pd.to_datetime(df["entryAt"])
            df = df.sort_values("entryAt")
            df["cumulative_pnl"] = df["pnl"].cumsum()

            # Metrics
            total_trades = len(df)
            wins = len(df[df["outcome"] == "win"])
            win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
            total_pnl = df["pnl"].sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Trades", total_trades)
            col2.metric("Win Rate", f"{win_rate:.1f}%")
            col3.metric("Total P&L", f"${total_pnl:.2f}")
            col4.metric("Profitable Trades", wins)

            st.markdown("---")

            # Equity Curve
            st.subheader("Equity Curve (Cumulative P&L)")
            fig = px.line(
                df,
                x="entryAt",
                y="cumulative_pnl",
                title="Account Growth Over Time",
                labels={"entryAt": "Date", "cumulative_pnl": "Cumulative P&L ($)"},
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Win/Loss Distribution
            st.subheader("Win/Loss Distribution by Asset Class")
            fig2 = px.histogram(
                df,
                x="assetClass",
                color="outcome",
                barmode="group",
                title="Trade Outcomes by Asset Class",
                template="plotly_dark",
            )
            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("View Raw Trade Data"):
                st.dataframe(
                    df[
                        [
                            "tradeId",
                            "asset",
                            "direction",
                            "entryPrice",
                            "exitPrice",
                            "pnl",
                            "outcome",
                        ]
                    ]
                )
        else:
            st.info("No trades found for this user. Make sure the User ID is correct.")

    with tab2:
        st.header("Behavioral AI Profiling")
        st.markdown(
            "We use advanced AI to detect hidden psychological patterns in your trading behavior."
        )

        if st.button("Generate Psychological Profile"):
            with st.spinner("Analyzing your trading history..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                resp = requests.get(
                    f"{API_URL}/api/profiling/{st.session_state.user_id}",
                    headers=headers,
                )

                if resp.status_code == 200:
                    profile = resp.json()
                    st.success("Profiling complete!")

                    st.subheader(
                        f"Detected Behavior: {profile.get('behavior', 'Unknown').replace('_', ' ').title()}"
                    )
                    st.write(
                        "**Summary:**", profile.get("summary", "No summary provided.")
                    )

                    st.markdown("### Evidence Log")
                    for ev in profile.get("evidence", []):
                        st.info(f"Session {ev['sessionId'][:8]}... -> {ev['reason']}")
                else:
                    st.error("Failed to fetch profiling data.")

    with tab3:
        st.header("Real-Time AI Coach")
        st.markdown(
            "Get actionable, real-time feedback based on your recent trading activity."
        )

        if len(st.session_state.trades_data) > 0:
            st.write(f"Ready to analyze {len(st.session_state.trades_data)} trades.")

            if st.button("Request Coaching Feedback"):
                with st.spinner("AI Coach is reviewing your trades..."):
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    # Send all trades for context
                    payload = {
                        "trades": st.session_state.trades_data[-20:]
                    }  # send last 20 for payload limits

                    resp = requests.post(
                        f"{API_URL}/api/coaching/{st.session_state.user_id}",
                        json=payload,
                        headers=headers,
                    )

                    if resp.status_code == 200:
                        coaching = resp.json()
                        st.markdown("### 🗣️ Coach's Message")
                        st.write(coaching.get("message", ""))

                        signals = coaching.get("signals", [])
                        if signals:
                            st.markdown("### ⚠️ Detected Risk Signals")
                            for s in signals:
                                st.warning(
                                    f"**{s['signal'].replace('_', ' ').title()}**: {s['reason']}"
                                )
                    else:
                        st.error("Failed to generate coaching feedback.")
        else:
            st.warning("No trades available for coaching.")
else:
    st.info("Please login using the sidebar to view your Trading Dashboard.")
