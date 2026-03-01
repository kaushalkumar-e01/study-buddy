import psutil
import time
import csv
from datetime import datetime

# Settings
STUDY_APPS = ["Code.exe", "python.exe", "Notion.exe"]
DATA_FILE = "study_session.csv"

def log_study_time(duration_seconds):
    date_today = datetime.now().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_today, duration_seconds])

def start_buddy():
    print("🎒 Study Buddy is tracking your time... Focus starts NOW!")
    total_seconds = 0
    
    try:
        while True:
            processes = [p.name() for p in psutil.process_iter(['name'])]
            is_studying = any(app in processes for app in STUDY_APPS)
            
            if is_studying:
                total_seconds += 10
                print(f"✅ Studying! Total today: {total_seconds // 60} mins")
            else:
                print("⚠️ Distracted! Timer paused.")
            
            # Save progress every 1 minute (60 seconds)
            if total_seconds % 60 == 0 and total_seconds > 0:
                log_study_time(60)
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print(f"\nSession ended. You studied for {total_seconds // 60} minutes today!")

if __name__ == "__main__":
    start_buddy()