import streamlit as st

# Page Configuration
st.set_page_config(page_title="Privacy Policy", page_icon="🔒", layout="wide")

# Apply Background Color & Hide Sidebar Initially (Requires `unsafe_allow_html=True`)
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f0fff0; /* Light green background */
        }
        [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)
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

# Sidebar (Only visible if logged in)
if "jwt_token" in st.session_state:
    with st.sidebar:
        st.header("📌 Navigation")
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

# Page Title
st.title("🔒 Privacy Policy & Terms of Service")

st.markdown("""
## **1. Introduction**
Welcome to **FarmBook**! Your privacy is important to us, and we are committed to protecting your personal information.  
This Privacy Policy explains how we collect, use, and safeguard your data when you use FarmBook.

---

## **2. Information We Collect**
We collect and store the following types of data:

### **a) Personal Information (Required for Account Creation)**
- **Username**
- **Email Address**
- **Encrypted Password**

### **b) Journal & Farming Data (Optional, Based on User Input)**
- **Crop Details** (Type, Season, Location, Sowing & Harvest Dates, Yield)
- **Financial Information** (Unit Price, Expenses, Profit/Loss)
- **Journal Notes** (Any additional farming-related observations)

### **c) Social Platform Data (If You Post Content)**
- **Posts** (Text, Images, Videos shared with the FarmBook community)
- **Comments** (User-generated comments on posts)
- **Likes** (Your interactions with other users' content)

### **d) System-Generated Data**
- **Analytics Data** (Farm profit trends, cost breakdowns, crop comparisons)
- **Crop Recommendation History** (Past crop suggestions based on input parameters)

### **e) Technical Data (Collected Automatically)**
- **Device Information** (Browser type, operating system)
- **IP Address** (For security & fraud prevention)
- **Usage Data** (Time spent on different pages, interactions with features)

---

## **3. How We Use Your Information**
We collect your data to:
✅ Provide core features like **journal management, crop recommendations, and analytics.**  
✅ Enable **secure authentication and user accounts.**  
✅ Improve **FarmBook's features through usage analytics.**  
✅ Facilitate **community interaction through posts, comments, and likes.**  
✅ Ensure **security and prevent unauthorized access.**  

🔒 **We do NOT sell your personal data.**  
🔄 **We may use anonymized data for research or improving our services.**  

---

## **4. Data Protection & Security**
We prioritize security with:
- **Industry-standard encryption** for stored passwords.
- **Access controls & authentication** to protect accounts.
- **Regular security audits** to prevent vulnerabilities.  

**However, no system is 100% secure.**  
Users should follow **best security practices** (e.g., strong passwords, logging out after use).

---

## **5. Third-Party Services**
FarmBook **does not share your data** with advertisers or third parties for commercial purposes.  
We **may disclose your data**:
- If required **by law** (e.g., court orders, government requests).
- To prevent **fraud, security breaches, or unauthorized activities**.

---

## **6. Crop Recommendation System Disclaimer**
Our **AI-powered Crop Recommendation System** suggests crops based on soil and weather conditions.  
However, **we do NOT guarantee accuracy**, and recommendations should be used **as a guideline, not a definitive decision**.

FarmBook is **not responsible for financial losses** due to recommendations.  
We strongly advise **consulting with local experts** before making farming decisions.

---

## **7. Your Rights & Data Control**
You have the right to:
- **Access & update** your personal data.
- **Delete your account & all associated data** upon request.
- **Opt-out** of analytics tracking (contact us for details).

---

## **8. Changes to This Policy**
We may update this Privacy Policy to reflect new features or legal requirements.  
If significant changes are made, **we will notify users via email or FarmBook notifications**.

---

## **9. Contact Us**
📩 **Email:** [your-email@example.com](mailto:your-email@example.com)  
If you have any questions or requests regarding your privacy, feel free to contact us.

""", unsafe_allow_html=True)
