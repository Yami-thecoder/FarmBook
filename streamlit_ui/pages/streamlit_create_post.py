import streamlit as st
from api import create_post

st.set_page_config(page_title="Create a Post", page_icon="📝", layout="wide")

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
    if st.button("➕ New Post"):
        st.switch_page("pages/streamlit_create_post.py")
    if st.button("📖 Manage Journal Entries"):
        st.switch_page("pages/streamlit_journal_view.py")
    if st.button("🌾 Crop Recommendation"):
        st.switch_page("pages/streamlit_crop.py")
    if st.button("🚪 Logout"):
        del st.session_state["jwt_token"]
        st.rerun()

st.title("➕ Create a New Post")

# Ensure user is logged in
if "jwt_token" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/streamlit_auth.py")

jwt_token = st.session_state["jwt_token"]

# Create Post Form
st.subheader("📤 Share what's on your mind")

post_title = st.text_input("Post Title", max_chars=100)  # Limit title to 100 characters
post_description = st.text_area("Post Description (Max 200 words)")  # ✅ Limit description

# Count words in description
word_count = len(post_description.split())
if word_count > 200:
    st.warning(f"⚠️ Your description has {word_count} words. The maximum allowed is 200.")

uploaded_file = st.file_uploader("Upload an image/video (Optional)", type=["jpg", "png", "mp4"])

# Validate before posting
if st.button("📤 Post"):
    if not post_title.strip():
        st.error("⚠️ A post must have a title.")
    elif not post_description.strip() and not uploaded_file:
        st.error("⚠️ A post must have either a description or a file.")
    elif word_count > 200:
        st.error("⚠️ Your post description exceeds the 200-word limit.")
    else:
        response = create_post(jwt_token, post_title, post_description, uploaded_file)
        if response:
            st.success("✅ Post Uploaded Successfully!")
            st.switch_page("pages/streamlit_posts.py")
            st.rerun()

