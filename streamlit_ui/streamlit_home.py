import streamlit as st
import base64
import os

# Set page configuration
st.set_page_config(page_title="FarmBook - Welcome", page_icon="🌱", layout="wide")

# Function to load local image as background

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# Use absolute path for local background image
BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "farm.jpeg")
BACKGROUND_IMAGE_BASE64 = get_base64_image(BACKGROUND_IMAGE_PATH)

# Apply background styling separately
if BACKGROUND_IMAGE_BASE64:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url('data:image/jpeg;base64,{BACKGROUND_IMAGE_BASE64}') no-repeat center center fixed;
                background-size: cover;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            .stApp {background-color: #f0fff0;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom styling
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .stButton>button {background-color: #2E7D32 !important; color: white !important; border-radius: 5px; padding: 10px 20px; font-size: 16px; border: none;}
        .stButton>button:hover {background-color: #1B5E20 !important;}
        .hero-container {display: flex; flex-direction: column; justify-content: center; align-items: center; height: 70vh; text-align: center; position: relative;}
        .hero-text {font-size: 4em; font-weight: bold; color: #2E7D32;}
        .tagline {font-size: 1.5em; color: #fff; margin-top: 10px;}
        .floating-login {position: fixed; bottom: 20px; right: 20px; z-index: 1000;}
        .feature-container {display: grid; grid-template-columns: 1fr 1fr; gap: 30px; padding: 30px; align-items: start; justify-content: center; width: 80%; margin: 10px;}
        .feature-card {background: rgba(255,255,255,0.95); padding: 40px; border-radius: 15px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); height: auto; width: 100%; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 50px;}
        .feature-card p {text-align: justify;}
        .footer {background: rgba(0,0,0,0.7); color: white; text-align: center; padding: 15px; border-radius: 5px; margin-top: 50px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar (Only visible if logged in)
if "jwt_token" in st.session_state:
    with st.sidebar:
        st.header("📌 FarmBook Navigation")
        if st.button("🏠 Home"): st.switch_page("streamlit_home.py")
        if st.button("📊 Dashboard"): st.switch_page("pages/streamlit_dashboard.py")
        if st.button("📢 Social Feed"): st.switch_page("pages/streamlit_posts.py")
        if st.button("📖 Manage Journal Entries"): st.switch_page("pages/streamlit_journal_view.py")
        if st.button("🌾 Crop Recommendation"): st.switch_page("pages/streamlit_crop.py")
        if st.button("🚪 Logout"):
            del st.session_state["jwt_token"]
            st.rerun()

# Hide sidebar if not logged in
if "jwt_token" not in st.session_state:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Hero Section
st.markdown("""
    <div class='hero-container'>
        <div>
            <div class='hero-text'>Welcome to FarmBook 🌱</div>
            <div class='tagline'>Your personal farming companion - Record, Analyze, and Connect!</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("<div class='feature-container'>", unsafe_allow_html=True)
features = [
    ("📖 Personal Journal", "Effortlessly track your farming activities and maintain a digital record of your journey. Log every sowing, harvest, and sale with detailed insights, ensuring you always have a clear view of your progress. No more lost notes—your farm’s history is now just a click away!"),
    ("📊 Analytics Dashboard", "Make data-driven decisions with real-time analytics. Monitor your farm’s financial health with profit and expense tracking, visualize trends over time, and optimize your yield for maximum efficiency. Empower yourself with insights that turn farming into smart farming!"),
    ("🤝 Community Posts", "Connect with fellow farmers, share experiences, and seek advice from the community. Whether it’s troubleshooting crop issues, discovering new techniques, or simply sharing a milestone, FarmBook fosters a vibrant and supportive network of farmers like you!"),
    ("🌾 Crop Recommendation", "Leverage AI-powered recommendations to choose the best crop based on soil health, climate conditions, and historical data. Boost your productivity and sustainability by growing crops that thrive in your region, reducing risks and maximizing returns!")
]

for i in range(0, len(features), 2):
    st.markdown(f"""
    <div style='display: flex; gap: 50px; justify-content: center; align-items: stretch; width: 100%;'>
        <div class='feature-card' style='flex: 1;'>
            <h3>{features[i][0]}</h3>
            <p>{features[i][1]}</p>
        </div>
        <div class='feature-card' style='flex: 1;'>
            <h3>{features[i+1][0]}</h3>
            <p>{features[i+1][1]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Login Button (Only if not logged in)
if "jwt_token" not in st.session_state:
    col1, col2, col3 = st.columns([4, 1, 4])
    with col2:
        if st.button("Login to explore"):
            st.switch_page("pages/streamlit_auth.py")


contact_email = "your-email@example.com"

# Footer with Correct Navigation
st.markdown(
    f"""
    <div class='footer'>
        <span>© 2025 FarmBook</span>
        <span style="margin: 0 10px;">|</span>
        <a href="?page=privacy" style="color: white; text-decoration: none; font-size: 16px;">📜 Privacy Policy</a>
        <span style="margin: 0 10px;">|</span>
        <a href="mailto:{contact_email}" style="color: white; text-decoration: none; font-size: 16px;">📩 Contact Us</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Correctly Retrieve Query Params Using st.query_params
query_params = st.query_params

# If Privacy Policy is Clicked, Switch Page
if query_params.get("page") == "privacy":
    st.switch_page("pages/streamlit_privacy.py")
