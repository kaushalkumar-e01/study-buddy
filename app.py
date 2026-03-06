import time
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





# Mistake Fix 1: Properly initialize Session State so timer persists
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'current_seconds' not in st.session_state:
    st.session_state.current_seconds = 0

st.divider()
st.subheader("⏳ Focus Timer")

col1, col2 = st.columns([1, 2])

with col1:
    # Mistake Fix 2: Disable input while running to prevent "jumping" time
    input_mins = st.number_input("Set Minutes", min_value=1, value=25, 
                                 disabled=st.session_state.current_seconds > 0)
    
    # Toggle logic: Button changes name and function based on state
    if not st.session_state.timer_running:
        button_label = "Resume" if st.session_state.current_seconds > 0 else "Start Focusing"
        if st.button(button_label, use_container_width=True):
            if st.session_state.current_seconds == 0:
                st.session_state.current_seconds = input_mins * 60
            st.session_state.timer_running = True
            st.rerun()
            
        # Reset button appears only when paused
        if st.session_state.current_seconds > 0:
            if st.button("Reset Timer", type="secondary", use_container_width=True):
                st.session_state.current_seconds = 0
                st.session_state.timer_running = False
                st.rerun()
    else:
        # Mistake Fix 3: Use a "Stop" button that breaks the loop immediately
        if st.button("Stop", type="primary", use_container_width=True):
            st.session_state.timer_running = False
            st.rerun()

with col2:
    if st.session_state.current_seconds > 0:
        empty_slot = st.empty()
        progress_bar = st.progress(0)
        total_possible = input_mins * 60
        
        # This while loop keeps the timer "alive" on the screen
        while st.session_state.current_seconds > 0 and st.session_state.timer_running:
            mins, secs = divmod(st.session_state.current_seconds, 60)
            empty_slot.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            
            # Update progress bar smoothly
            progress_val = 1.0 - (st.session_state.current_seconds / total_possible)
            progress_bar.progress(min(progress_val, 1.0))
            
            time.sleep(1)
            st.session_state.current_seconds -= 1
            
            if st.session_state.current_seconds == 0:
                st.session_state.timer_running = False
                st.success("Session complete! Great work, Kaushalkumar. ☕")
                st.rerun()
        
        # If the user clicked stop, show the time exactly where it froze
        if not st.session_state.timer_running and st.session_state.current_seconds > 0:
            mins, secs = divmod(st.session_state.current_seconds, 60)
            empty_slot.metric("Time Paused", f"{mins:02d}:{secs:02d}")
    else:
        st.info("Ready for a session? Set your time and hit Start!")