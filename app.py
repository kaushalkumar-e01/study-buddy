import time
import datetime
import requests
import streamlit as st
import streamlit.components.v1 as components
import csv
import os
import pandas as pd

# --- 1. DATA LOGIC ---
LOG_FILE = "study_data.csv"
DEADLINE_FILE = "deadlines.csv"

def save_study_data(subject, notes):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Subject", "Notes"])
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d"), subject, notes])

def save_deadline(task, date):
    file_exists = os.path.isfile(DEADLINE_FILE)
    with open(DEADLINE_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Task", "Deadline"])
        writer.writerow([task, str(date)])

def get_deadlines():
    if os.path.isfile(DEADLINE_FILE):
        df = pd.read_csv(DEADLINE_FILE)
        df['Deadline'] = pd.to_datetime(df['Deadline'])
        df['Days Left'] = (df['Deadline'] - pd.Timestamp.now().normalize()).dt.days
        return df.sort_values(by="Deadline")
    return pd.DataFrame()

def get_daily_sticky_quote():
    try:
        response = requests.get("https://zenquotes.io/api/today", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"“{data[0]['q']}” – {data[0]['a']}"
        return "“The best way to predict the future is to invent it.” – Alan Kay"
    except:
        return "“Keep pushing forward, Kaushalkumar!”"

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Study Buddy", page_icon="🎒", layout="wide", initial_sidebar_state="collapsed")

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000000 100%) !important;
        color: #ffffff;
    }
    .stButton > button {
        border: 1px solid rgba(76, 161, 175, 0.4) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 8px 20px !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        border-color: #4ca1af !important;
        box-shadow: 0 0 10px rgba(76, 161, 175, 0.5);
    }
    [data-testid="stNotification"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    [data-testid="stNotificationContentSuccess"] { border-left: 5px solid #64ffda !important; }
    [data-testid="stNotificationContentInfo"] { border-left: 5px solid #4ca1af !important; }
    
    .journal-section {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    thead tr th:first-child, tbody tr th:first-child, tbody tr td:first-child { display: none !important; }
    h1, h2, h3, p, label, .stMarkdown { color: #ffffff !important; }
    .greeting-text { font-size: 32px; font-weight: bold; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

col1, col2, col3, _ = st.columns([1, 1, 1, 5]) 
with col1:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = "Home"
with col2:
    if st.button("📚 Journal", use_container_width=True): st.session_state.page = "Study Journal"
with col3:
    if st.button("ℹ️ About", use_container_width=True): st.session_state.page = "About"

page = st.session_state.page
st.divider()

# --- 5. SHARED JOURNAL UI ---
def show_journal_ui():
    st.subheader("📝 Secure Study Journal")
    with st.form(f"study_form_{st.session_state.page}", clear_on_submit=True):
        sub = st.text_input("What subject did you study?", placeholder="e.g., Python, C")
        note = st.text_area("Key takeaways for today:")
        if st.form_submit_button("Lock in Journal"):
            if sub and note:
                save_study_data(sub, note)
                st.success(f"✅ Saved {sub} progress!")
            else: st.warning("Please fill in both.")
    if st.checkbox("Show my past study entries", key=f"check_{st.session_state.page}"):
        if os.path.isfile(LOG_FILE):
            st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True, hide_index=True)

# --- 6. PAGE CONTENT ---
if page == "Home":
    st.markdown(f'<div class="greeting-text">Hello, Kaushalkumar! 👋</div>', unsafe_allow_html=True)
    st.info(f"💡 **Today's Inspiration:** {get_daily_sticky_quote()}")

    # Deadlines Section
    st.subheader("🎯 Active Missions (Deadlines)")
    with st.expander("➕ Add New Deadline"):
        with st.form("deadline_form", clear_on_submit=True):
            task_name = st.text_input("Task Name")
            d_date = st.date_input("Due Date")
            if st.form_submit_button("Deploy Deadline"):
                if task_name:
                    save_deadline(task_name, d_date)
                    st.rerun()
    df_d = get_deadlines()
    if not df_d.empty:
        for _, row in df_d.iterrows():
            days = row['Days Left']
            color = "#e74c3c" if days <= 3 else "#4ca1af" 
            st.markdown(f"""
                <div style="border-left: 5px solid {color}; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <span style="font-weight: bold; font-size: 18px; color: white;">{row['Task']}</span>
                    <span style="float: right; background: {color}; padding: 2px 10px; border-radius: 20px; font-size: 12px;">{days} Days Left</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No pending missions.")

    st.divider()
    show_journal_ui()

    # TIMER & STOPWATCH 
    st.divider()
    components.html("""
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; font-family: 'Segoe UI'; color: white; text-align: center;">
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; width: 45%; min-width: 280px;">
            <h3>⏳ Focus Timer</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin: 10px 0;">
                <button onclick="changeT(-60)" style="width:30px; height:30px; border-radius:50%; border:1px solid #4ca1af; background:transparent; color:#4ca1af; cursor:pointer;">-</button>
                <h1 id="t" style="font-size: 50px; color: #4ca1af; margin: 0; min-width: 130px;">25:00</h1>
                <button onclick="changeT(60)" style="width:30px; height:30px; border-radius:50%; border:1px solid #4ca1af; background:transparent; color:#4ca1af; cursor:pointer;">+</button>
            </div>
            <button onclick="startT()" style="background:#4ca1af; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Start</button>
            <button onclick="pauseT()" style="background:#e67e22; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Pause</button>
            <button onclick="resetT()" style="background:#e74c3c; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Reset</button>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; width: 45%; min-width: 280px;">
            <h3>⏱️ Session Stopwatch</h3>
            <h1 id="s" style="font-size: 50px; color: #4ca1af; margin: 10px 0;">00:00:00</h1>
            <button onclick="startS()" style="background:#4ca1af; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Start</button>
            <button onclick="pauseS()" style="background:#e67e22; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Pause</button>
            <button onclick="resetS()" style="background:#95a5a6; border:none; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; margin:2px;">Clear</button>
        </div>
    </div>
    <script>
    let tl=1500, tid=null, stime=0, sid=null;
    function updateTD(){ let m=Math.floor(tl/60), s=tl%60; document.getElementById('t').innerText=(m<10?"0":"")+m+":"+(s<10?"0":"")+s; }
    function changeT(v){ if(!tid && tl+v >= 60) { tl+=v; updateTD(); } }
    function startT(){ if(!tid) tid=setInterval(()=>{ if(tl>0){tl--; updateTD();} else {clearInterval(tid); tid=null;} },1000); }
    function pauseT(){ clearInterval(tid); tid=null; }
    function resetT(){ pauseT(); tl=1500; updateTD(); }
    function updateSD(){ let h=Math.floor(stime/3600), m=Math.floor((stime%3600)/60), s=stime%60; document.getElementById('s').innerText=(h<10?"0":"")+h+":"+(m<10?"0":"")+m+":"+(s<10?"0":"")+s; }
    function startS(){ if(!sid) sid=setInterval(()=>{stime++; updateSD();},1000); }
    function pauseS(){ clearInterval(sid); sid=null; }
    function resetS(){ pauseS(); stime=0; updateSD(); }
    </script>
    """, height=280)

elif page == "Study Journal":
    show_journal_ui()

elif page == "About":
    st.title("About Study Buddy")
    st.write("A professional CSE productivity portal built by Kaushalkumar at BMSCE.")