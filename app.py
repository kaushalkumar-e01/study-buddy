import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Study Buddy", page_icon="🎒", layout="wide",initial_sidebar_state="collapsed")

# 2. Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .greeting-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 8px solid #4CAF50;
        margin-bottom: 25px;
    }
    .greeting-text {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 28px;
        font-weight: bold;
    }
    .menu-header {
        color: #4CAF50;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Menu
with st.sidebar:
    st.markdown('<p class="menu-header">📌 Main Menu</p>', unsafe_allow_html=True)
    page = st.radio("", ["Home",  "About"], label_visibility="collapsed")

# 4. Main Page Content
if page == "Home":
    # Custom HTML Greeting Card
    st.markdown(f"""
        <div class="greeting-card">
            <div class="greeting-text">Hello, Kaushalkumar! 👋</div>
            <p style="color: #7f8c8d; font-size: 18px;">
                Welcome to your personalized <b>Study Buddy</b> portal. 
                Everything is set up and ready for your next big feature.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Simple Layout for the rest of the home page
    col1, col2 = st.columns(2)
    with col1:
        st.info("🚀 **Project Mission**\nCreating a secure and simple productivity tool for students.")
    with col2:
        st.success("🛠️ **Status**\nFrontend structure is live. Logic will be added later.")


elif page == "About":
    st.title("📖 About Study Buddy")
    st.write("A professional-grade productivity application designed by Kaushalkumar.")