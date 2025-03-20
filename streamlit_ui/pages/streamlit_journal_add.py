import streamlit as st
from api import add_journal_entry
import datetime

st.set_page_config(page_title="Add New Journal Entry", page_icon="➕", layout="wide")

# Custom Styling for Buttons Only and hide default navigation bar
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .stButton>button {background-color: #2E7D32 !important; color: white !important; border-radius: 5px; transition: background-color 0.3s ease;}
        .stButton>button:hover {background-color: #1B5E20 !important;}
    </style>
    """,
    unsafe_allow_html=True
)

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

# Sidebar Navigation
with st.sidebar:
    st.header("📌 FarmBook Navigation")
    if st.button("🏠 Home"):
        st.switch_page("streamlit_home.py")
    if st.button("📊 Dashboard"):
        st.switch_page("pages/streamlit_dashboard.py")
    if st.button("📢 Social Feed"):
        st.switch_page("pages/streamlit_posts.py")
    if st.button("📖 View Journal Entries"):
        st.switch_page("pages/streamlit_journal_view.py")
    if st.button("➕ Add New Entry"):
        st.switch_page("pages/streamlit_journal_add.py")
    if st.button("✏️ Edit Entry"):
        st.switch_page("pages/streamlit_journal_edit.py")
    if st.button("🌾 Crop Recommendation"):
        st.switch_page("pages/streamlit_crop.py")
    if st.button("🚪 Logout"):
        del st.session_state["jwt_token"]
        st.rerun()

# Check if user is logged in
if "jwt_token" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/streamlit_auth.py")

st.title("Add New Journal Entry")

# Form for adding a new journal entry
crop_name = st.text_input("Crop Name")
season = st.text_input("Season")
farm_location = st.text_input("Farm Location")
sowing_date = st.date_input("Sowing Date", value=None)
harvest_date = st.date_input("Harvest Date", value=None)
harvest_date = harvest_date if harvest_date else None
yield_amount = st.number_input("Yield (kg)", min_value=0.0, step=0.1, format="%.1f")
sold_amount = st.number_input("Sold Amount (kg)", min_value=0.0, step=0.1, format="%.1f")
unit_price = st.number_input("Unit Price (Rs. per kg)", min_value=0.0, step=0.1, format="%.2f")
expenses = st.number_input("Total Expenses (Rs.)", min_value=0.0, step=0.1, format="%.2f")
notes = st.text_area("Notes")

# Validation for required fields
if st.button("Add Entry"):
    if not crop_name or not season or not farm_location or not sowing_date:
        st.error("Crop Name, Season, Farm Location, and Sowing Date are required fields.")
    else:
        current_date = datetime.date.today()
        if sowing_date > current_date:
            st.error("Sowing date cannot be in the future.")
        elif harvest_date and harvest_date > current_date:
            st.error("Harvest date cannot be in the future.")
        elif harvest_date and harvest_date < sowing_date:
            st.error("Harvest date cannot be earlier than sowing date.")
        else:
            response = add_journal_entry(
                st.session_state['jwt_token'], crop_name, season, farm_location,
                str(sowing_date), str(harvest_date) if harvest_date else None, yield_amount, sold_amount,
                unit_price, expenses, notes
            )
            if response:
                st.success("New entry added successfully!")
                st.switch_page("pages/streamlit_journal_view.py")
            else:
                st.error("Failed to add entry. Please try again.")
