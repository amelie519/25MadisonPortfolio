from metrics import compute_metrics

ids = [6962181067, 2347167796, 5577150313, 5553957443,
       2026352035, 4020332650, 8792009665]

for uid in ids:
    m = compute_metrics(uid)
    print(uid, "| steps:", m["avg_daily_steps"],
          "| sleep:", m["avg_sleep_hours"],
          "| weeknight sleep:", m["weeknight_sleep_hours"],
          "| resting HR:", m["resting_hr"],
          "| anchors:", m["anchor_hours"])

          