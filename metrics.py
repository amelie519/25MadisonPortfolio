import pandas as pd

USER_ID = 5553957443  # demo user


def load(path, time_col, uid):
    df = pd.read_csv(path)
    df = df[df["Id"] == uid].copy()
    df[time_col] = pd.to_datetime(df[time_col], format="mixed")
    return df


def compute_metrics(uid=USER_ID):
    steps = load("sample_data/hourlySteps_merged.csv", "ActivityHour", uid)
    sleep = load("sample_data/minuteSleep_merged.csv", "date", uid)
    hr = load("sample_data/heartrate_seconds_merged.csv", "Time", uid)

    m = {"user_id": uid}

    # --- Steps ---
    steps["day"] = steps["ActivityHour"].dt.normalize()
    daily = steps.groupby("day")["StepTotal"].sum()
    is_weekend = daily.index.dayofweek >= 5
    m["avg_daily_steps"] = round(daily.mean())
    m["weekday_steps"] = round(daily[~is_weekend].mean())
    m["weekend_steps"] = round(daily[is_weekend].mean())

    # --- Sleep (value 1 = asleep) ---
    asleep = sleep[sleep["value"] == 1].copy()
    # shift back 12h so a night that crosses midnight counts as one night
    asleep["night"] = (asleep["date"] - pd.Timedelta(hours=12)).dt.normalize()
    hours = asleep.groupby("night").size() / 60
    hours = hours[hours >= 3]  # drop partial nights at the edges of the data
    weekend_night = hours.index.dayofweek.isin([4, 5])  # Fri and Sat nights
    m["avg_sleep_hours"] = round(hours.mean(), 2)
    m["weeknight_sleep_hours"] = round(hours[~weekend_night].mean(), 2)
    m["weekend_night_sleep_hours"] = round(hours[weekend_night].mean(), 2)
    m["sleep_nights"] = int(len(hours))

    # --- Approximate resting heart rate (10th percentile of each day) ---
    hr["day"] = hr["Time"].dt.normalize()
    m["hr_days"] = int(hr["day"].nunique())
    if m["hr_days"] >= 3:
        m["resting_hr"] = round(hr.groupby("day")["Value"].quantile(0.1).mean())
    else:
        m["resting_hr"] = None  # too little data

    # --- Routine anchors: hours of day that are active on most days ---
    steps["hour"] = steps["ActivityHour"].dt.hour
    by_hour = steps.groupby("hour")["StepTotal"]
    active_share = by_hour.apply(lambda s: (s >= 250).mean())
    avg_steps = by_hour.mean()
    anchors = active_share[(active_share >= 0.5) & (avg_steps >= 300)]
    m["anchor_hours"] = [int(h) for h in anchors.index]

    return m


if __name__ == "__main__":
    for key, value in compute_metrics().items():
        print(key, ":", value)
