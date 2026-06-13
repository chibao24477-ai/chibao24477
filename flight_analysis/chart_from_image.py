# -*- coding: utf-8 -*-
"""5月 vs 6月 每日旅客量比較圖。
B欄=5月(整月)；C欄=6月(只到日12，今日13號尚無後續)。
日1因截圖被切掉，兩月皆缺(5月日1可由月總額回推=7498)。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False

# day: 旅客量
MAY = {2:6005,3:5513,4:6092,5:6621,6:6992,7:6348,8:6700,9:7297,10:7089,11:7127,
       12:6581,13:6497,14:6650,15:6748,16:7437,17:7169,18:6596,19:6445,20:6739,
       21:6792,22:6802,23:7216,24:6945,25:6505,26:6266,27:5914,28:6350,29:6345,
       30:7241,31:6455}
JUN = {2:6197,3:6536,4:6846,5:7257,6:8012,7:7097,8:6951,9:6152,10:7407,11:7336,12:8264}

MAY_C, JUN_C = "#2f6db5", "#f0884a"

# === 圖1：每日走勢 ===
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(list(MAY), list(MAY.values()), marker="o", ms=4, color=MAY_C, label="5 月")
ax.plot(list(JUN), list(JUN.values()), marker="s", ms=4, color=JUN_C, label="6 月（至 12 號）")
for d, v in MAY.items():
    ax.annotate(f"{v}", (d, v), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=6.5, color=MAY_C)
for d, v in JUN.items():
    ax.annotate(f"{v}", (d, v), textcoords="offset points", xytext=(0, -12),
                ha="center", fontsize=6.5, color="#c4622d")
ax.set_title("每日旅客量走勢：5 月 vs 6 月", fontsize=15)
ax.set_xlabel("日"); ax.set_ylabel("旅客量（人）")
ax.set_xticks(range(1, 32))
ax.legend(fontsize=12); ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("flight_analysis/output/01_每日旅客量_5月vs6月.png", dpi=140, bbox_inches="tight")

# === 圖2：1~12號 同期(MTD)比較 ===
days = range(2, 13)  # 兩月都有資料的範圍
may_mtd = sum(MAY[d] for d in days)
jun_mtd = sum(JUN[d] for d in days)
diff = jun_mtd - may_mtd
pct = diff / may_mtd * 100

fig2, ax2 = plt.subplots(figsize=(6, 5))
bars = ax2.bar(["5 月\n(2~12號)", "6 月\n(2~12號)"], [may_mtd, jun_mtd],
               color=[MAY_C, JUN_C], width=0.55)
ax2.bar_label(bars, fmt="{:,.0f}", padding=4, fontsize=12)
ax2.set_title(f"旅客量同期比較（2~12 號）\n6 月較 5 月 {diff:+,}（{pct:+.1f}%）", fontsize=13)
ax2.set_ylabel("旅客量（人）")
ax2.margins(y=0.15)
ax2.spines[["top", "right"]].set_visible(False)
fig2.tight_layout()
fig2.savefig("flight_analysis/output/02_旅客量同期比較_2to12.png", dpi=140, bbox_inches="tight")

print(f"5月 2~12號 合計={may_mtd:,}")
print(f"6月 2~12號 合計={jun_mtd:,}")
print(f"差異={diff:+,}（{pct:+.1f}%）")
print("輸出：01_每日旅客量_5月vs6月.png / 02_旅客量同期比較_2to12.png")
