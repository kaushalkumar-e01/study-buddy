import time
import streamlit as st
import base64

def play_sound():
    # Ensure 'timer_sound.mp3' is in your project folder!
    sound_url = "timer_sound.mp3" 
    html_string = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(html_string, height=0)

# 1. Page Config
st.set_page_config(page_title="Study Buddy", page_icon="🎒", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom CSS (Your existing CSS remains the same)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
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
    .menu-header { color: #4CAF50; font-size: 20px; font-weight: 600; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Menu
with st.sidebar:
    st.markdown('<p class="menu-header">📌 Main Menu</p>', unsafe_allow_html=True)
    page = st.radio("", ["Home", "About"], label_visibility="collapsed")

# 4. Main Page Content
if page == "Home":
    st.markdown(f"""
        <div class="greeting-card">
            <div class="greeting-text">Hello, Kaushalkumar! 👋</div>
            <p style="color: #7f8c8d; font-size: 18px;">
                Welcome to your personalized <b>Study Buddy</b> portal. 
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("🚀 **Project Mission**\nCreating a secure productivity tool.")
    with col2:
        st.success("🛠️ **Status**\nLogic is active and running.")

    # --- TIMER SECTION ---
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'current_seconds' not in st.session_state:
        st.session_state.current_seconds = 0

    st.divider()
    st.subheader("⏳ Focus Timer")

    t_col1, t_col2 = st.columns([1, 2])

    with t_col1:
        input_mins = st.number_input("Set Minutes", min_value=1, value=25, 
                                     disabled=st.session_state.current_seconds > 0)
        
        if not st.session_state.timer_running:
            btn_label = "Resume" if st.session_state.current_seconds > 0 else "Start Focusing"
            if st.button(btn_label, use_container_width=True):
                if st.session_state.current_seconds == 0:
                    st.session_state.current_seconds = input_mins * 60
                st.session_state.timer_running = True
                st.rerun()
                
            if st.session_state.current_seconds > 0:
                if st.button("Reset Timer", type="secondary", use_container_width=True):
                    st.session_state.current_seconds = 0
                    st.session_state.timer_running = False
                    st.rerun()
        else:
            if st.button("Stop", type="primary", use_container_width=True):
                st.session_state.timer_running = False
                st.rerun()

    with t_col2:
        if st.session_state.current_seconds > 0:
            empty_slot = st.empty()
            progress_bar = st.progress(0)
            total_possible = input_mins * 60
            
            while st.session_state.current_seconds > 0 and st.session_state.timer_running:
                mins, secs = divmod(st.session_state.current_seconds, 60)
                empty_slot.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
                progress_val = 1.0 - (st.session_state.current_seconds / total_possible)
                progress_bar.progress(min(progress_val, 1.0))
                
                time.sleep(1)
                st.session_state.current_seconds -= 1
                
                # Completion Logic inside the loop
                if st.session_state.current_seconds == 0:
                    st.session_state.timer_running = False
                    empty_slot.metric("Time Remaining", "00:00")
                    progress_bar.progress(1.0)
                    st.success("🎉 Session complete! Great work, Kaushalkumar. ☕")
                    play_sound()
                    time.sleep(2)
                    st.session_state.current_seconds = 0
                    st.rerun()
            
            # If manually stopped
            if not st.session_state.timer_running and st.session_state.current_seconds > 0:
                mins, secs = divmod(st.session_state.current_seconds, 60)
                empty_slot.metric("Time Paused", f"{mins:02d}:{secs:02d}")
        else:
            st.info("Ready for a session? Set your time and hit Start!")

elif page == "About":
    st.title("📖 About Study Buddy")
    st.write("A professional-grade productivity application designed by Kaushalkumar.")