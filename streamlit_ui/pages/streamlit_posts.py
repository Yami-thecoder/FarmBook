import streamlit as st
import os
from api import fetch_posts, fetch_text_file, like_post, comment_on_post, API_URL

st.set_page_config(page_title="FarmBook - Social Feed", page_icon="📢", layout="wide")

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

st.title("📢 FarmBook Social Feed")

# Ensure user is logged in
if "jwt_token" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/streamlit_auth.py")

jwt_token = st.session_state["jwt_token"]

# Fetch Posts
posts = fetch_posts(jwt_token)

if posts:
    for post in posts:
       with st.expander(f"📝 {post['title']} by {post['username']} (posted on {post['created_at']})"):
            # Display post description
            if "description" in post and post["description"]:
                st.write(f"✏️ {post['description']}")

            # Display uploaded file
            if "file_url" in post and post["file_url"]:
                file_url = f"{API_URL}{post['file_url']}"
                file_extension = os.path.splitext(file_url)[1].lower()

                if file_extension in [".jpg", ".png", ".jpeg"]:
                    st.image(file_url, use_container_width=True)
                elif file_extension in [".mp4", ".mov"]:
                    st.video(file_url)
                elif file_extension == ".txt":
                    file_content = fetch_text_file(file_url)
                    if file_content:
                        st.text_area("📜 Text File Content:", file_content, height=200, disabled=True)
                    else:
                        st.error("⚠️ Unable to load text file.")
                else:
                    st.warning("⚠️ Unsupported file format.")

            # Like Button
            if st.button(f"👍 {post['likes']}", key=f"like_{post['id']}"):
                if like_post(jwt_token, post['id']):
                    st.rerun()

            # Unique key for each post's comment input
            comment_key = f"comment_input_{post['id']}"

            # Initialize session state for comment input
            if comment_key not in st.session_state:
                st.session_state[comment_key] = ""

            # Comment Input Field
            comment_text = st.text_input("Write a comment", key=comment_key)

            # Comment Submission Button
            if st.button("💬 Comment", key=f"comment_{post['id']}"):
                if comment_text.strip():
                    if comment_on_post(jwt_token, post['id'], comment_text):
                        del st.session_state[comment_key]  # ✅ Remove input key to reset field
                        st.rerun()  # ✅ Refresh UI to show new comment and clear field

            # Display Comments
            if post["comments"]:
                # ✅ Sort comments again (just in case)
                sorted_comments = sorted(post["comments"], key=lambda x: x['created_at'], reverse=True)

                # ✅ Display Comments (latest first)
                if sorted_comments:
                    st.write("💬 **Latest Comments:**")
                    for comment in sorted_comments:
                        st.write(f"👉 **{comment['username']}**: {comment['content']} ({comment['created_at']})")

            st.markdown("---")
else:
    st.info("ℹ️ No posts available yet.")
