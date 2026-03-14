import time
import datetime
import requests
import streamlit as st
import streamlit.components.v1 as components
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

    st.divider()
   # --- UPGRADED DUAL TRACKER WITH INLINE MESSAGE ---
    dual_tracker_html = """
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; font-family: 'Segoe UI', Tahoma, sans-serif; color: #2c3e50;">
        <div style="text-align: center; background: rgba(255, 255, 255, 0.4); padding: 30px; border-radius: 15px; width: 45%; min-width: 300px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <h3 style="margin-top: 0; color: #34495e;">⏳ Focus Timer</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin: 15px 0;">
                <button onclick="adjustTime(-60)" style="width: 35px; height: 35px; border-radius: 50%; border: 2px solid #4ca1af; background: transparent; color: #4ca1af; font-weight: bold; cursor: pointer;">-</button>
                <h1 id="timer-display" style="font-size: 50px; margin: 0; color: #4ca1af; min-width: 140px;">25:00</h1>
                <button onclick="adjustTime(60)" style="width: 35px; height: 35px; border-radius: 50%; border: 2px solid #4ca1af; background: transparent; color: #4ca1af; font-weight: bold; cursor: pointer;">+</button>
            </div>
            <div>
                <button onclick="startTimer()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #4ca1af; color: white; font-weight: bold; cursor: pointer;">Start</button>
                <button onclick="stopTimer()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #e74c3c; color: white; font-weight: bold; cursor: pointer;">Pause</button>
                <button onclick="resetTimer()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #95a5a6; color: white; font-weight: bold; cursor: pointer;">Reset</button>
            </div>
            <p id="timer-msg" style="color: #4ca1af; font-weight: bold; margin-top: 15px; display: none; font-size: 14px;">🎉 Session complete! Great work, Kaushalkumar.</p>
        </div>
        <div style="text-align: center; background: rgba(255, 255, 255, 0.4); padding: 30px; border-radius: 15px; width: 45%; min-width: 300px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <h3 style="margin-top: 0; color: #34495e;">⏱️ Session Stopwatch</h3>
            <h1 id="sw-display" style="font-size: 50px; margin: 15px 0; color: #4ca1af;">00:00:00</h1>
            <div>
                <button onclick="startSW()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #4ca1af; color: white; font-weight: bold; cursor: pointer;">Start</button>
                <button onclick="stopSW()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #e74c3c; color: white; font-weight: bold; cursor: pointer;">Pause</button>
                <button onclick="resetSW()" style="padding: 10px 15px; margin: 5px; border-radius: 8px; border: none; background: #95a5a6; color: white; font-weight: bold; cursor: pointer;">Clear</button>
            </div>
        </div>
    </div>
    <script>
        let timeLeft = 1500; let timerId = null;
        function updateTimer() {
            let m = Math.floor(timeLeft / 60); let s = timeLeft % 60;
            document.getElementById('timer-display').innerText = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
        }
        function adjustTime(amount) {
            if (!timerId) { if (timeLeft + amount >= 60) { timeLeft += amount; updateTimer(); document.getElementById('timer-msg').style.display = 'none'; } }
        }
        function startTimer() {
            if (!timerId) {
                document.getElementById('timer-msg').style.display = 'none';
                timerId = setInterval(() => {
                    if (timeLeft > 0) { timeLeft--; updateTimer(); } 
                    else { clearInterval(timerId); timerId = null; document.getElementById('timer-msg').style.display = 'block'; }
                }, 1000);
            }
        }
        function stopTimer() { clearInterval(timerId); timerId = null; }
        function resetTimer() { stopTimer(); timeLeft = 1500; updateTimer(); document.getElementById('timer-msg').style.display = 'none'; }
        let swTime = 0; let swId = null;
        function updateSW() {
            let h = Math.floor(swTime / 3600); let m = Math.floor((swTime % 3600) / 60); let s = swTime % 60;
            document.getElementById('sw-display').innerText = (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
        }
        function startSW() { if (!swId) { swId = setInterval(() => { swTime++; updateSW(); }, 1000); } }
        function stopSW() { clearInterval(swId); swId = null; }
        function resetSW() { stopSW(); swTime = 0; updateSW(); }
    </script>
    """
    import streamlit.components.v1 as components
    components.html(dual_tracker_html, height=350)


# --- E. Secure Study Journal---
#st.divider()
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