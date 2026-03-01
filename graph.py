import pandas as pd
import matplotlib.pyplot as plt

def show_my_progress():
    try:
        # Load the data
        df = pd.read_csv("study_session.csv", names=["Date", "Seconds"])
        
        # Group by date and convert seconds to minutes
        daily_stats = df.groupby("Date")["Seconds"].sum() / 60
        
        # Create the graph
        daily_stats.plot(kind='bar', color='skyblue')
        plt.title("My Study Progress (Minutes per Day)")
        plt.xlabel("Date")
        plt.ylabel("Minutes")
        plt.show()
    except FileNotFoundError:
        print("No data found yet! Start studying first.")

if __name__ == "__main__":
    show_my_progress()