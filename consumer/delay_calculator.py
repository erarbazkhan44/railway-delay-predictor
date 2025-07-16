import pandas as pd
from datetime import datetime

def calculate_delay(row):
    fmt = "%H:%M"
    t1 = datetime.strptime(row['scheduled_time'], fmt)
    t2 = datetime.strptime(row['actual_time'], fmt)
    return int((t2 - t1).total_seconds() / 60)

def main():
    df = pd.read_csv("data/raw_delays.csv")  # ✅ Corrected path
    df['delay_minutes'] = df.apply(calculate_delay, axis=1)

    print("📊 Train Delays:\n")
    print(df[['train_no', 'station', 'scheduled_time', 'actual_time', 'delay_minutes']])

if __name__ == "__main__":
    main()
