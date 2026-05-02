import time
import datetime
import requests
import streamlit as st
import streamlit.components.v1 as components
import csv
import os
import pandas as pd
import updates

# --- 1. DATA LOGIC (Preserved) ---
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

# --- 3. CUSTOM CSS (Preserved) ---
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
    .greeting-text { font-size: 32px; font-weight: bold; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

col1, col2, col3, col4, _ = st.columns([1, 1, 1.2, 1, 3.8]) 
with col1:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = "Home"
with col2:
    if st.button("📚 Journal", use_container_width=True): st.session_state.page = "Study Journal"
with col3:
    if st.button("🌐 Global Stats", use_container_width=True): st.session_state.page = "Global Stats"
with col4:
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

elif page == "Global Stats":
    st.markdown('<div class="greeting-text">🇮🇳 India Live Dashboard</div>', unsafe_allow_html=True)
    
    st.subheader("📊 Indian Market & Finance")
    mkt = updates.get_market_data()
    m_col1, m_col2, m_col3 = st.columns(3)
    
    m_col1.metric("Nifty 50", mkt['Nifty'])
    m_col2.metric("Sensex", mkt['Sensex'])
    m_col3.metric("USD / INR", mkt['USD_INR'])

    st.divider()
    
    st.subheader("❓ Today in Indian History")
    today_date = str(datetime.datetime.now().date())
    if "daily_q" not in st.session_state or st.session_state.get("q_date") != today_date:
        st.session_state.daily_q = updates.get_live_question()
        st.session_state.q_date = today_date
    
    gk = st.session_state.daily_q
    st.info(f"📅 **On this day:** {gk['q']}")
    st.success(f"📖 **The Fact:** {gk['a']}")

    st.divider()
    
    st.subheader("📰 Top India Headlines")
    india_news = updates.get_india_news()
    if india_news:
        for item in india_news:
            st.markdown(f"📍 [{item['title']}]({item['link']})")
    else:
        st.error("⚠️ Unable to fetch news. Please check your connection.")

elif page == "Study Journal":
    show_journal_ui()

elif page == "About":
    st.markdown('<div class="greeting-text">System Information & Portfolio</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="journal-section">', unsafe_allow_html=True)
    
    # --- Professional Header ---
    st.title("🎒 Study Buddy v2.0")
    st.markdown("""
    **Study Buddy** is a centralized productivity ecosystem designed to streamline the academic workflow of 
    Computer Science Engineering students. Developed with a focus on efficiency, it integrates real-time 
    financial analytics, global intelligence, and rigorous session tracking into a single dark-mode interface.
    """)
    
    st.divider()
    
    # --- Developer & Core Mission ---
    col_dev, col_miss = st.columns(2)
    
    with col_dev:
        st.subheader("👨‍💻 Developer Profile")
        st.write("**Name:** Kaushalkumar")
        st.write("**Affiliation:** CSE Department, BMSCE Bangalore")
        st.write("**Focus:** Backend Architecture & Algorithmic Logic")
        
    with col_miss:
        st.subheader("🎯 Project Mission")
        st.write("To reduce cognitive load by centralizing essential academic tools—Deadlines, Daily Logs, and Global Context—into a high-performance dashboard.")

    st.divider()

    # --- Technical Stack (Professional Grid) ---
    st.subheader("💻 Technical Architecture")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    
    with t_col1:
        st.code("Streamlit\n(Frontend Framework)")
    with t_col2:
        st.code("Python 3.12\n(Logic Engine)")
    with t_col3:
        st.code("Pandas/CSV\n(Data Persistence)")
    with t_col4:
        st.code("REST APIs\n(Live Intelligence)")

    st.divider()

    # --- Footer Note ---
    st.caption("© 2026 | Engineered for Academic Excellence at BMS College of Engineering.")
    
    st.markdown('</div>', unsafe_allow_html=True)