import pandas as pd

steps = pd.read_csv("sample_data/hourlySteps_merged.csv")
sleep = pd.read_csv("sample_data/minuteSleep_merged.csv")
hr = pd.read_csv("sample_data/heartrate_seconds_merged.csv")
daily = pd.read_csv("sample_data/dailyActivity_merged.csv")

def days_per_user(df, col):
    d = pd.to_datetime(df[col], format="mixed").dt.date
    return df.assign(day=d).groupby("Id")["day"].nunique()

summary = pd.DataFrame({
    "steps_days": days_per_user(steps, "ActivityHour"),
    "sleep_days": days_per_user(sleep, "date"),
    "hr_days": days_per_user(hr, "Time"),
    "daily_days": days_per_user(daily, "ActivityDate"),
}).dropna()

print(summary.sort_values("sleep_days", ascending=False).head(10))