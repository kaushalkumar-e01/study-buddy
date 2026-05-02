import time
import datetime
import requests
import streamlit as st
import streamlit.components.v1 as components
import csv
import os
import pandas as pd
import updates

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

def remove_deadline(task_to_remove):
    """Removes a specific task from the CSV and refreshes the UI."""
    if os.path.isfile(DEADLINE_FILE):
        df = pd.read_csv(DEADLINE_FILE)
        df = df[df['Task'] != task_to_remove]
        df.to_csv(DEADLINE_FILE, index=False)
        st.rerun()

def get_deadlines():
    if os.path.isfile(DEADLINE_FILE):
        df = pd.read_csv(DEADLINE_FILE)
        df['Deadline'] = pd.to_datetime(df['Deadline'])
        today = pd.Timestamp.now().normalize()
        df['Days Left'] = (df['Deadline'] - today).dt.days
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
        for index, row in df_d.iterrows():
            days = row['Days Left']
            if days < 0:
                status_text = f"⚠️ {abs(days)} Days Overdue"
                color = "#ff4b4b" 
            elif days == 0:
                status_text = "🔥 Due Today"
                color = "#ffa500" 
            else:
                status_text = f"⏳ {days} Days Left"
                color = "#4ca1af" if days > 3 else "#e74c3c"

            d_col, b_col = st.columns([8, 2])
            with d_col:
                st.markdown(f"""
                    <div style="border-left: 5px solid {color}; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px;">
                        <span style="font-weight: bold; font-size: 18px; color: white;">{row['Task']}</span>
                        <span style="float: right; color: {color}; font-weight: bold;">{status_text}</span>
                    </div>
                """, unsafe_allow_html=True)
            with b_col:
                if st.button("✅ Done", key=f"done_{index}", use_container_width=True):
                    remove_deadline(row['Task'])
            st.write("") 
    else:
        st.write("No pending missions.")

    st.divider()
    show_journal_ui()

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
    st.markdown('<div class="greeting-text">Developer Portfolio & System Specifications</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="journal-section">', unsafe_allow_html=True)
        
        # --- Project Identity ---
        st.title("🎒 Study Buddy | Academic OS")
        st.markdown("""
        **Study Buddy** is a bespoke productivity ecosystem engineered for the specific workflows of 
        Computer Science Engineering students. It centralizes volatile data—market analytics, 
        global news, and mission-critical deadlines—into a single, low-latency dashboard.
        """)
        
        st.divider()
        
        # --- Professional Credentials ---
        col_dev, col_edu = st.columns(2)
        
        with col_dev:
            st.subheader("👨‍💻 Engineering Lead")
            st.write("**Name:** Kaushalkumar")
            st.write("**Specialization:** Backend Development & System Architecture")
            st.write("**Status:** Year I, Computer Science Engineering (Semester 2)")
            
        with col_edu:
            st.subheader("🏫 Institutional Affiliation")
            st.write("**College:** BMS College of Engineering (BMSCE), Bangalore")
            st.write("**Department:** Department of Computer Science & Engineering")
            st.write("**Location:** Bull Temple Rd, Basavanagudi")
            
        st.divider()

        # --- Technical Stack (CSE Taxonomy) ---
        st.subheader("💻 Core Technical Stack")
        t1, t2, t3, t4 = st.columns(4)
        
        with t1:
            st.info("**Framework**")
            st.code("Streamlit v1.41")
        with t2:
            st.info("**Environment**")
            st.code("Python 3.12")
        with t3:
            st.info("**Persistence**")
            st.code("CSV / Pandas")
        with t4:
            st.info("**Integration**")
            st.code("RESTful APIs")

        st.divider()

        # --- Vision ---
        st.subheader("🎯 Core Mission")
        st.write("""
        The primary objective of this project is to optimize **Cognitive Resource Management**. 
        By reducing the 'search cost' for academic deadlines and external context (Markets/News), 
        the user can maintain a high-state of 'Deep Work' efficiency.
        """)
        
        st.divider()
        st.caption("© 2026 | Developed by Kaushalkumar for BMSCE CSE Portfolio.")
        st.markdown('</div>', unsafe_allow_html=True)