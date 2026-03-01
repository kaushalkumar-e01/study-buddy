import streamlit as st
import pandas as pd
import psutil
import time
from datetime import datetime

st.title("🎒 Study Buddy Web")

# --- SIDEBAR CONTROL ---
st.sidebar.header("Controls")
if st.sidebar.button("Start Tracking Session"):
    st.sidebar.success("Tracking Active! (Minimize this window and study)")
    # This is where your main.py logic lives now!
    STUDY_APPS = ["Code.exe", "python.exe"]
    
    # Simple loop to log 1 minute of 'demo' data
    processes = [p.name() for p in psutil.process_iter(['name'])]
    if any(app in processes for app in STUDY_APPS):
        with open("study_session.csv", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d')},60\n")
        st.sidebar.write("✅ Logged 1 minute!")

# --- MAIN DASHBOARD ---
try:
    df = pd.read_csv("study_session.csv", names=["Date", "Seconds"])
    daily_stats = df.groupby("Date")["Seconds"].sum() / 60
    st.bar_chart(daily_stats)
except:
    st.info("Click 'Start Tracking' to begin your first session!")