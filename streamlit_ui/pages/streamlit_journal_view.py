import streamlit as st
import pandas as pd
from api import fetch_journal_entries, export_pdf_report

st.set_page_config(page_title="View Journal Entries", page_icon="📖", layout="wide")

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

# Custom Sidebar for Navigation
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

st.title("Your Journal Entries")

# Export to PDF Button at the Start
if st.button("Export as PDF"):
    pdf_content = export_pdf_report(st.session_state['jwt_token'])
    if pdf_content:
        st.download_button(
            label="Download PDF",
            data=pdf_content,
            file_name="farm_journal.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Failed to generate PDF report.")

# Fetch Journal Entries
data = fetch_journal_entries(st.session_state['jwt_token'])
if data:
    journal_data = pd.DataFrame(data)
else:
    journal_data = pd.DataFrame(columns=["id", "crop_name", "season", "farm_location", "sowing_date", "harvest_date", "yield_amount", "sold_amount", "unit_price", "expenses", "total_revenue", "profit", "notes"])

# Display Entries
st.dataframe(journal_data.set_index("id"), use_container_width=True)
