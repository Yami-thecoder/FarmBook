import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from api import fetch_profit_trend, fetch_crop_comparison, fetch_cost_breakdown, export_pdf_report

st.set_page_config(page_title="Farmbook Dashboard", page_icon="📊", layout="wide")

# Custom Sidebar
with st.sidebar:
    # st.image("logo.png", width=150)  # Placeholder for logo
    st.header("📌 FarmBook Navigation")
    if st.button("🏠 Home"):
        st.switch_page("streamlit_home.py")
    if st.button("📊 Dashboard"):
        st.switch_page("pages/streamlit_dashboard.py")
    if st.button("📢 Social Feed"):
        st.switch_page("pages/streamlit_posts.py")
    if st.button("📖 Manage Journal Entries"):
        st.switch_page("pages/streamlit_journal_view.py")
    if st.button("🌾 Crop Recommendation"):
        st.switch_page("pages/streamlit_crop.py")
    if st.button("🚪 Logout"):
        del st.session_state["jwt_token"]
        st.rerun()

# Hide Default Streamlit Page Navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .stButton>button {background-color: #2E7D32 !important; color: white !important; border-radius: 5px; transition: background-color 0.3s ease;}
        .stButton>button:hover {background-color: #1B5E20 !important;}
    </style>
    """, unsafe_allow_html=True)

# Apply the background color
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: #f0fff0; /* Light green background */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Check if user is logged in
if "jwt_token" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/streamlit_auth.py")

# Dashboard Layout
st.title("Farmbook Dashboard")
st.subheader("Profit Trends Over Time")

# Fetch Profit Trend Data
data = fetch_profit_trend(st.session_state['jwt_token'])
if data:
    dates = [entry["sowing_date"] for entry in data]
    profits = [entry["profit"] for entry in data]

    # Plot the Profit Trend
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted chart size
    ax.plot(dates, profits, marker="o", linestyle="-", color="b")
    ax.set_xlabel("Sowing Date")
    ax.set_ylabel("Profit (Rs.)")
    ax.set_title("Profit Trend Over Time", fontsize=12)
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No profit data available.")

# Crop Comparison
st.subheader("Crop Comparison - Total Profit")
data = fetch_crop_comparison(st.session_state['jwt_token'])
if data:
    crops = [entry["crop_name"] for entry in data]
    profits = [entry["total_profit"] for entry in data]

    # Plot Crop Comparison
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted chart size
    ax.bar(crops, profits, color="g")
    ax.set_xlabel("Crops")
    ax.set_ylabel("Total Profit (Rs.)")
    ax.set_title("Crop Comparison - Profit", fontsize=12)
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("No crop comparison data available.")

# Cost Breakdown
st.subheader("Cost Breakdown")
# Fetch Cost Breakdown Data
data = fetch_cost_breakdown(st.session_state['jwt_token'])

if data:
    crops = [entry["crop_name"] for entry in data]
    expenses = [entry["total_expenses"] for entry in data]

    # ✅ Convert None and NaN values to 0
    expenses = [0 if (x is None or isinstance(x, float) and np.isnan(x)) else x for x in expenses]

    # ✅ Check if all values in expenses are now valid
    if all(x == 0 for x in expenses):
        st.warning("No valid cost data available to display.")
    else:
        # Plot Cost Breakdown
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.pie(expenses, labels=crops, autopct="%1.1f%%", startangle=140, colors=["r", "b", "g", "y", "c"], radius=0.7)
        ax.set_title("Cost Breakdown by Crop", fontsize=10)
        st.pyplot(fig)
else:
    st.warning("No cost breakdown data available.")
