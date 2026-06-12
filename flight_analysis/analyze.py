# -*- coding: utf-8 -*-
"""航班月報分析：環比(上月)、年同期(去年同月) 比較 + 趨勢圖。
只比較三項：航班數、旅客量、金額。

輸入：flight_analysis/flights.csv
欄位：date, flight_no, passengers, amount  (每列=某天某航班一次起飛)

輸出：
  - 終端機文字報表
  - flight_analysis/output/*.png 趨勢圖
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 設定中文字型
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False

# 設定要比較的三個月（本月 / 上月 / 去年同月）
CUR   = (2026, 5)   # 本月
PREV  = (2026, 4)   # 上月
YOY   = (2025, 5)   # 去年同月
LABELS = {CUR: "本月", PREV: "上月", YOY: "去年同月"}

df = pd.read_csv("flight_analysis/flights.csv", parse_dates=["date"])
df["ym"] = df["date"].dt.to_period("M")
df["day"] = df["date"].dt.day


def month_summary(period):
    p = pd.Period(f"{period[0]}-{period[1]:02d}", freq="M")
    sub = df[df["ym"] == p]
    return dict(
        flights=len(sub),
        pax=int(sub["passengers"].sum()),
        amount=int(sub["amount"].sum()),
    )


def pct(a, b):
    return (a - b) / b * 100 if b else 0


cur, prev, yoy = month_summary(CUR), month_summary(PREV), month_summary(YOY)


def diff_block(title, a, b):
    """a=本月, b=對比月"""
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    print(f"{'指標':<10}{'本月':>14}{'對比月':>14}{'差異':>12}{'增減%':>10}")
    print("-" * 60)
    rows = [
        ("航班數", a["flights"], b["flights"], "{:+d}"),
        ("旅客量", a["pax"], b["pax"], "{:+,d}"),
        ("金額", a["amount"], b["amount"], "{:+,d}"),
    ]
    for name, av, bv, f in rows:
        print(f"{name:<11}{av:>14,}{bv:>14,}{f.format(av-bv):>14}{pct(av,bv):>+9.1f}%")


# === 要求 1：與上月比較 ===
diff_block("【要求 1】本月 vs 上月（環比）", cur, prev)

# === 要求 2：與去年同月比較 ===
diff_block("【要求 2】本月 vs 去年同月（年同期 YoY）", cur, yoy)

# === 要求 3：圖表 ===
months_order = [YOY, PREV, CUR]
labels = [LABELS[m] for m in months_order]
summ = {m: month_summary(m) for m in months_order}

# 圖1：三月份 航班數/旅客量/金額 並列長條圖
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
metrics = [("flights", "航班數（班）"), ("pax", "旅客量（人）"), ("amount", "金額（元）")]
colors = ["#9bb3d4", "#6f9bd1", "#2f6db5"]
for ax, (key, title) in zip(axes, metrics):
    vals = [summ[m][key] for m in months_order]
    bars = ax.bar(labels, vals, color=colors)
    ax.set_title(title, fontsize=13)
    ax.bar_label(bars, fmt="{:,.0f}", padding=3, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.margins(y=0.18)
fig.suptitle("三月份比較：去年同月 / 上月 / 本月", fontsize=15, y=1.02)
fig.tight_layout()
fig.savefig("flight_analysis/output/01_月份比較.png", dpi=130, bbox_inches="tight")

# 圖2：本月 / 上月 / 去年同月 每日金額走勢
fig2, ax = plt.subplots(figsize=(13, 4.8))
for m, c, lab in [(YOY, "#9bb3d4", "去年同月"), (PREV, "#f0a868", "上月"), (CUR, "#2f6db5", "本月")]:
    p = pd.Period(f"{m[0]}-{m[1]:02d}", freq="M")
    daily = df[df["ym"] == p].groupby("day")["amount"].sum()
    ax.plot(daily.index, daily.values, marker="o", ms=3, color=c, label=f"{lab}金額")
ax.set_title("每日金額走勢：本月 vs 上月 vs 去年同月", fontsize=14)
ax.set_xlabel("日"); ax.set_ylabel("當日金額（元）")
ax.legend(); ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.set_major_formatter(lambda x, _: f"{x/1e6:.1f}M")
fig2.tight_layout()
fig2.savefig("flight_analysis/output/02_每日金額走勢.png", dpi=130, bbox_inches="tight")

print("\n圖表已輸出至 flight_analysis/output/：")
print("  01_月份比較.png / 02_每日金額走勢.png")
