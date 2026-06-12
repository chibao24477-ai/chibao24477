# -*- coding: utf-8 -*-
"""航班月報分析：環比(上月)、年同期(去年同月) 比較 + 趨勢圖。

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
        load=sub["passengers"].mean() / 180,            # 平均載客率
        yield_per_pax=sub["amount"].sum() / sub["passengers"].sum(),  # 客單價
    )


def pct(a, b):
    return (a - b) / b * 100 if b else 0


def fmt_money(x):
    return f"{x:,.0f}"


cur, prev, yoy = month_summary(CUR), month_summary(PREV), month_summary(YOY)


def diff_block(title, a, b):
    """a=本月, b=對比月"""
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    print(f"{'指標':<10}{'本月':>14}{'對比月':>14}{'差異':>12}{'增減%':>10}")
    print("-" * 60)
    rows = [
        ("航班數", a["flights"], b["flights"], "{:+d}"),
        ("旅客量", a["pax"], b["pax"], "{:+,d}"),
        ("金額(營收)", a["amount"], b["amount"], "{:+,d}"),
    ]
    for name, av, bv, f in rows:
        print(f"{name:<11}{av:>14,}{bv:>14,}{f.format(av-bv):>14}{pct(av,bv):>+9.1f}%")
    print(f"{'平均載客率':<9}{a['load']*100:>13.1f}%{b['load']*100:>13.1f}%"
          f"{(a['load']-b['load'])*100:>+13.1f}{'':>10}")
    print(f"{'客單價':<10}{a['yield_per_pax']:>14,.0f}{b['yield_per_pax']:>14,.0f}"
          f"{a['yield_per_pax']-b['yield_per_pax']:>+14,.0f}"
          f"{pct(a['yield_per_pax'],b['yield_per_pax']):>+9.1f}%")


# === 要求 1：與上月比較 ===
diff_block("【要求 1】本月 vs 上月（環比）", cur, prev)
print("""
可能造成差異的原因（依資料拆解）：
  • 量的成長：本月航班數較上月增加 → 加班機/旺季排班，帶動旅客量上升。
  • 價的成長：客單價上升 → 票價調漲或高艙等／旺季票占比提高。
  • 載客率上升 → 需求轉強（連假、季節因素），空位減少。
  ※ 金額差異可拆成「量(旅客)效果 × 價(客單價)效果」兩部分，見下方拆解圖。""")

# === 要求 2：與去年同月比較 ===
diff_block("【要求 2】本月 vs 去年同月（年同期 YoY）", cur, yoy)
print("""
可能造成差異的原因（依資料拆解）：
  • 與去年同月相比，航班數/旅客量同步成長 → 航線運能擴張或市場復甦。
  • 客單價年增 → 票價結構調整、通膨反映於票價、燃油附加費等。
  • 載客率年增 → 整體需求回升，去年同期基期較低。""")

# === 量價拆解（解釋金額差異的主因）===
def decompose(a, b, name):
    pax_effect = (a["pax"] - b["pax"]) * b["yield_per_pax"]      # 量效果
    price_effect = (a["yield_per_pax"] - b["yield_per_pax"]) * a["pax"]  # 價效果
    print(f"\n金額差異拆解（本月 vs {name}）：總差異 {fmt_money(a['amount']-b['amount'])}")
    print(f"  ├─ 旅客量(量)貢獻：{fmt_money(pax_effect)}")
    print(f"  └─ 客單價(價)貢獻：{fmt_money(price_effect)}")
    return pax_effect, price_effect

dec_prev = decompose(cur, prev, "上月")
dec_yoy = decompose(cur, yoy, "去年同月")

# === 要求 3：圖表 ===
months_order = [YOY, PREV, CUR]
labels = [LABELS[m] for m in months_order]
summ = {m: month_summary(m) for m in months_order}

# 圖1：三月份 航班數/旅客量/金額 並列長條圖
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
metrics = [("flights", "航班數（班）"), ("pax", "旅客量（人）"), ("amount", "金額（營收, 元）")]
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

# 圖2：本月 vs 上月 每日金額走勢
fig2, ax = plt.subplots(figsize=(13, 4.8))
for m, c, lab in [(PREV, "#f0a868", "上月"), (CUR, "#2f6db5", "本月")]:
    p = pd.Period(f"{m[0]}-{m[1]:02d}", freq="M")
    daily = df[df["ym"] == p].groupby("day")["amount"].sum()
    ax.plot(daily.index, daily.values, marker="o", ms=3, color=c, label=f"{lab}金額")
ax.set_title("每日金額走勢：本月 vs 上月", fontsize=14)
ax.set_xlabel("日"); ax.set_ylabel("當日金額（元）")
ax.legend(); ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.set_major_formatter(lambda x, _: f"{x/1e6:.1f}M")
fig2.tight_layout()
fig2.savefig("flight_analysis/output/02_每日金額走勢.png", dpi=130, bbox_inches="tight")

# 圖3：金額差異 量價拆解 瀑布圖（本月 vs 上月）
fig3, ax = plt.subplots(figsize=(8.5, 5))
base = prev["amount"]
pax_e, price_e = dec_prev
steps = ["上月金額", "旅客量貢獻", "客單價貢獻", "本月金額"]
vals = [base, pax_e, price_e, cur["amount"]]
cum = [0, base, base + pax_e, 0]
heights = [base, pax_e, price_e, cur["amount"]]
cols = ["#888", "#5aa469" if pax_e >= 0 else "#c0504d",
        "#5aa469" if price_e >= 0 else "#c0504d", "#2f6db5"]
for i, (s, h, b, c) in enumerate(zip(steps, heights, cum, cols)):
    ax.bar(s, h, bottom=b, color=c)
    ax.text(i, b + h + (cur["amount"]*0.01), f"{h:+,.0f}" if 0 < i < 3 else f"{h:,.0f}",
            ha="center", fontsize=9)
ax.set_title("金額差異拆解（本月 vs 上月）：量 × 價", fontsize=14)
ax.set_ylabel("金額（元）")
ax.yaxis.set_major_formatter(lambda x, _: f"{x/1e6:.0f}M")
ax.spines[["top", "right"]].set_visible(False)
fig3.tight_layout()
fig3.savefig("flight_analysis/output/03_量價拆解瀑布圖.png", dpi=130, bbox_inches="tight")

print("\n圖表已輸出至 flight_analysis/output/：")
print("  01_月份比較.png / 02_每日金額走勢.png / 03_量價拆解瀑布圖.png")
