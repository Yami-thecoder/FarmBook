import streamlit as st
import numpy as np
import pickle
import os

# Streamlit UI
st.set_page_config(page_title="Crop Recommendation", page_icon="🌱", layout="wide")

# Check if user is logged in
if "jwt_token" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/streamlit_auth.py")

# Display Loading Message
loading_message = st.empty()
loading_message.markdown("### Loading Crop Recommendation System... Please wait ⏳")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")
STAND_SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "standscaler.pkl")
MINMAX_SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "minmaxscaler.pkl")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)
with open(STAND_SCALER_PATH, "rb") as standscaler_file:
    standscaler = pickle.load(standscaler_file)
with open(MINMAX_SCALER_PATH, "rb") as minmaxscaler_file:
    minmaxscaler = pickle.load(minmaxscaler_file)

# Remove Loading Message
loading_message.empty()

# Crop Dictionary
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# Sidebar Navigation
with st.sidebar:
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
            background-color: #f0fff0 !important; /* Light green background */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌱 Crop Recommendation System")
st.markdown("### Enter Soil and Climate Conditions")

# Form Inputs
col1, col2, col3 = st.columns(3)
with col1:
    nitrogen = st.number_input("Nitrogen", min_value=0.0, step=0.1, format="%.1f")
    phosphorus = st.number_input("Phosphorus", min_value=0.0, step=0.1, format="%.1f")
    potassium = st.number_input("Potassium", min_value=0.0, step=0.1, format="%.1f")
with col2:
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, step=0.1, format="%.1f")
    humidity = st.number_input("Humidity (%)", min_value=0.0, step=0.1, format="%.1f")
with col3:
    ph = st.number_input("pH Level", min_value=0.0, step=0.1, format="%.1f")
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, step=0.1, format="%.1f")

# Predict Button
if st.button("🌿 Get Recommendation"):
    feature_list = np.array([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]).reshape(1, -1)
    scaled_features = minmaxscaler.transform(feature_list)
    final_features = standscaler.transform(scaled_features)
    prediction = model.predict(final_features)
    
    recommended_crop = crop_dict.get(prediction[0], "Unknown Crop")
    st.success(f"✅ Recommended Crop: **{recommended_crop}**")
    
    # Display Recommendation Card
    st.markdown(
        f"""
        <div style="background-color:#2E7D32;color:white;padding:20px;border-radius:10px;text-align:center;margin-top:20px;">
            <h2>🌾 {recommended_crop} is the best crop to cultivate! 🌾</h2>
        </div>
        """, unsafe_allow_html=True
    )
