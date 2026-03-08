import time
import datetime
import requests
import streamlit as st

# --- 1. FUNCTIONS ---
def play_sound():
    # Ensure 'timer_sound.mp3' is in your project folder!
    sound_url = "timer_sound.mp3" 
    html_string = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(html_string, height=0)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Study Buddy", page_icon="🎒", layout="wide", initial_sidebar_state="collapsed")

# --- 3. CUSTOM CSS ---
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
    .stopwatch-display {
        font-family: 'Courier New', Courier, monospace;
        color: #4CAF50; font-size: 50px; font-weight: bold;
        background: #2c3e50; padding: 10px 20px; border-radius: 10px;
        text-align: center; border: 2px solid #ecf0f1; margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR MENU ---
with st.sidebar:
    st.markdown('<p class="menu-header">📌 Main Menu</p>', unsafe_allow_html=True)
    page = st.radio("", ["Home", "About"], label_visibility="collapsed")

# --- 5. MAIN PAGE CONTENT ---
if page == "Home":
    # A. Greeting Card
    st.markdown(f"""
        <div class="greeting-card">
            <div class="greeting-text">Hello, Kaushalkumar! 👋</div>
            <p style="color: #7f8c8d; font-size: 18px;">
                Welcome to your personalized <b>Study Buddy</b> portal. 
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("🚀 **Project Mission**\nCreating a secure productivity tool.")
    with col_info2:
        st.success("🛠️ **Status**\nLogic is active and running.")

    
# --- B. Daily Quotes Section (Internet Version) ---
    st.divider()
    st.subheader("💡 Today's Inspiration")

    def get_daily_sticky_quote():
        try:
            # We use the '/today' endpoint instead of '/random'
            response = requests.get("https://zenquotes.io/api/today")
            if response.status_code == 200:
                data = response.json()
                # This data only changes once every 24 hours at the server level
                return f"“{data[0]['q']}” – {data[0]['a']}"
            else:
                return "“The best way to predict the future is to invent it.” – Alan Kay"
        except Exception:
            return "“Keep pushing forward, Kaushalkumar!”"

    # Display the quote
    st.info(get_daily_sticky_quote())


    # C. Timer Section
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
                m, s = divmod(st.session_state.current_seconds, 60)
                empty_slot.metric("Time Remaining", f"{m:02d}:{s:02d}")
                progress_bar.progress(min(1.0 - (st.session_state.current_seconds / total_possible), 1.0))
                time.sleep(1)
                st.session_state.current_seconds -= 1
                if st.session_state.current_seconds == 0:
                    st.session_state.timer_running = False
                    st.success("🎉 Session complete! Great work, Kaushalkumar. ☕")
                    play_sound()
                    time.sleep(2)
                    st.rerun()
            if not st.session_state.timer_running and st.session_state.current_seconds > 0:
                m, s = divmod(st.session_state.current_seconds, 60)
                empty_slot.metric("Time Paused", f"{m:02d}:{s:02d}")
        else:
            st.info("Ready for a session?")

    # D. Stopwatch Section
    if 'sw_running' not in st.session_state:
        st.session_state.sw_running = False
    if 'sw_seconds' not in st.session_state:
        st.session_state.sw_seconds = 0

    st.divider()
    st.subheader("⏱️ Session Stopwatch")
    sw_col1, sw_col2 = st.columns([1, 2])

    with sw_col1:
        if not st.session_state.sw_running:
            if st.button("Start Tracking", use_container_width=True, type="primary"):
                st.session_state.sw_running = True
                st.rerun()
            if st.session_state.sw_seconds > 0:
                if st.button("Clear Stopwatch", use_container_width=True):
                    st.session_state.sw_seconds = 0
                    st.rerun()
        else:
            if st.button("Stop Tracking", use_container_width=True):
                st.session_state.sw_running = False
                st.rerun()

    with sw_col2:
        sw_display = st.empty()
        while st.session_state.sw_running:
            mm, ss = divmod(st.session_state.sw_seconds, 60)
            hh, mm = divmod(mm, 60)
            sw_display.markdown(f'<div class="stopwatch-display">{hh:02d}:{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            st.session_state.sw_seconds += 1
        mm, ss = divmod(st.session_state.sw_seconds, 60)
        hh, mm = divmod(mm, 60)
        sw_display.markdown(f'<div class="stopwatch-display">{hh:02d}:{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)

elif page == "About":
    st.title("📖 About Study Buddy")
    st.write("A professional-grade productivity application designed by Kaushalkumar.")