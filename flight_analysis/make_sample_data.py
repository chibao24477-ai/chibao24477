# -*- coding: utf-8 -*-
"""產生模擬航班資料，僅供示範報表格式之用。
真實使用時，把這份 CSV 換成你的實際資料即可（欄位不變）。
欄位：date(日期), flight_no(航班編號), passengers(旅客數), amount(金額)
每一列 = 某天某航班的一次起飛。
"""
import csv, random, calendar
from datetime import date

random.seed(42)

# 三個要比較的月份：去年同月、上月、本月
MONTHS = [(2025, 5), (2026, 4), (2026, 5)]
FLIGHTS = ["BR101", "BR102", "JX201", "CI303", "GE361"]

# 各月份的「基準」設定，用來模擬出可解讀的差異
profile = {
    (2025, 5): dict(base_amt=2300, load=0.78, daily_flights=4),   # 去年同月
    (2026, 4): dict(base_amt=2450, load=0.81, daily_flights=4),   # 上月
    (2026, 5): dict(base_amt=2780, load=0.88, daily_flights=5),   # 本月：漲價+加班機+旺季
}

rows = []
for (y, m) in MONTHS:
    p = profile[(y, m)]
    ndays = calendar.monthrange(y, m)[1]
    for d in range(1, ndays + 1):
        dow = date(y, m, d).weekday()
        # 週末班次與載客率較高
        weekend = dow >= 4
        nflights = p["daily_flights"] + (1 if weekend else 0)
        for i in range(nflights):
            fno = FLIGHTS[i % len(FLIGHTS)]
            load = min(0.99, random.gauss(p["load"] + (0.05 if weekend else 0), 0.06))
            seats = 180
            pax = max(40, int(seats * load))
            price = random.gauss(p["base_amt"], 180) * (1.12 if weekend else 1.0)
            amount = int(pax * price)
            rows.append([date(y, m, d).isoformat(), fno, pax, amount])

with open("flight_analysis/flights.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["date", "flight_no", "passengers", "amount"])
    w.writerows(rows)

print(f"已產生 {len(rows)} 筆模擬資料 -> flight_analysis/flights.csv")
