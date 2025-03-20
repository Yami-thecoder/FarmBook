import streamlit as st
import pandas as pd
from api import fetch_journal_entries, update_journal_entry, delete_journal_entry

st.set_page_config(page_title="Edit Journal Entry", page_icon="✏️", layout="wide")

# Custom Styling for Buttons and Hiding Default Navigation
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

st.title("Edit Journal Entry")

# Fetch Journal Entries
data = fetch_journal_entries(st.session_state['jwt_token'])
if data:
    journal_data = pd.DataFrame(data)
else:
    journal_data = pd.DataFrame(columns=["id", "crop_name", "season", "farm_location", "sowing_date", "harvest_date", "yield_amount", "sold_amount", "unit_price", "expenses", "notes"])

# Select Entry to Edit
if not journal_data.empty:
    entry_id = st.selectbox("Select an Entry to Edit", ["Select an entry"] + list(journal_data["id"].values))
    if entry_id and entry_id != "Select an entry":
        entry = journal_data[journal_data["id"] == entry_id].iloc[0]
        
        # Edit Form
        crop_name = st.text_input("Crop Name", entry["crop_name"])
        season = st.text_input("Season", entry["season"])
        farm_location = st.text_input("Farm Location", entry["farm_location"])
        sowing_date = st.date_input("Sowing Date", pd.to_datetime(entry["sowing_date"]))
        harvest_date = st.date_input("Harvest Date", pd.to_datetime(entry["harvest_date"]) if entry["harvest_date"] else None)
        yield_amount = st.number_input("Yield (kg)", min_value=0.0, value=float(entry["yield_amount"]))
        sold_amount = st.number_input("Sold Amount (kg)", min_value=0.0, value=float(entry["sold_amount"]))
        unit_price = st.number_input("Unit Price (Rs. per kg)", min_value=0.0, value=float(entry["unit_price"]))
        expenses = st.number_input("Total Expenses (Rs.)", min_value=0.0, value=float(entry["expenses"]))
        notes = st.text_area("Notes", entry["notes"])
        
        # Update Entry
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Entry"):
                response = update_journal_entry(
                    st.session_state['jwt_token'], entry_id, crop_name, season, farm_location,
                    str(sowing_date), str(harvest_date) if harvest_date else None, yield_amount, sold_amount,
                    unit_price, expenses, notes
                )
                if response:
                    st.success("Entry updated successfully!")
                    st.switch_page("pages/streamlit_journal_view.py")
                else:
                    st.error("Failed to update entry. Please try again.")
        
        with col2:
            if st.button("Delete Entry"):
                response = delete_journal_entry(st.session_state['jwt_token'], entry_id)
                if response:
                    st.error("Entry deleted successfully!")
                    st.switch_page("pages/streamlit_journal_view.py")
                else:
                    st.error("Failed to delete entry. Please try again.")
