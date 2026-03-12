import time
import datetime
import requests
import streamlit as st
import csv
import os

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
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stApp {
        background: transparent;
    }
    
    .greeting-text {
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 800;
        background: -webkit-linear-gradient(#2c3e50, #4ca1af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }      
    
    /* 1. FORCE BUTTONS TO THE LEFT */
    [data-testid="column"] {
        display: flex;
        justify-content: flex-start !important; /* Changed from 'center' to 'flex-start' */
        align-items: center;
        width: fit-content !important; /* Makes columns only as wide as the button */
        flex: unset !important;
        min-width: unset !important;
    }

    /* 2. CLEAN BUTTON STYLE */
    .stButton > button {
        border: none !important;
        background: transparent !important;
        padding-left: 0px !important; /* Removes left gap */
        padding-right: 20px !important; /* Adds space between buttons */
        transition: transform 0.2s ease !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px); /* Slight lift instead of scale */
        color: #4ca1af !important;
        background: transparent !important;
    }

    /* 3. HIDE THAT EXTRA BAR */
    /* If you see a white line or bar, this ensures the container is invisible */
    .nav-container, .glass-nav, .glass-card {
        display: none !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
# --- TOP NAVIGATION LOGIC ---
# 1. Initialize 'page' if it doesn't exist yet
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# 2. Create the buttons
col1, col2, col3, col_spacer = st.columns([1, 1, 1, 5]) 

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
with col2:
    if st.button("📚 Journal", use_container_width=True):
        st.session_state.page = "Study Journal"
with col3:
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"

# 3. Now assign the variable (This is where your error was)
page = st.session_state.page

st.divider()
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




# --- E. Secure Study Journal---
st.divider()
st.subheader("📝 Secure Study Journal")

LOG_FILE = "study_data.csv"

# Function to save data remains the same
def save_study_data(subject, notes):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Subject", "Notes"])
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d"), subject, notes])

# We use a form to group the inputs
with st.form("study_form", clear_on_submit=True):
    # 1. Text input for the subject instead of a selectbox
    sub = st.text_input("What subject did you study?", placeholder="e.g., Python, C, AR Research")
    note = st.text_area("Key takeaways for today:")
    submit = st.form_submit_button("Lock in Journal")

    if submit:
        if sub and note:
            save_study_data(sub, note)
            
            # 2. Logic to show message and make it disappear
            msg_container = st.empty() # Create a placeholder
            msg_container.success(f"✅ Securely saved your {sub} progress!")
            time.sleep(2) # Wait for 2 seconds
            msg_container.empty() # Clear the message
        else:
            st.warning("Please fill in both the subject and notes.")

# View Past Logs logic remains the same
if st.checkbox("Show my past study entries"):
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode='r') as f:
            st.table(csv.DictReader(f))
    else:
        st.info("No logs found yet.")