# -*- coding: utf-8 -*-
"""依使用者截圖(分頁2026)轉錄的每日資料畫比較圖。
B欄=整月每日數值；C欄=只有日2~12。日1因截圖被切掉，未納入。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False

# day: value
B = {2:6005,3:5513,4:6092,5:6621,6:6992,7:6348,8:6700,9:7297,10:7089,11:7127,
     12:6581,13:6497,14:6650,15:6748,16:7437,17:7169,18:6596,19:6445,20:6739,
     21:6792,22:6802,23:7216,24:6945,25:6505,26:6266,27:5914,28:6350,29:6345,
     30:7241,31:6455}
C = {2:6197,3:6536,4:6846,5:7257,6:8012,7:7097,8:6951,9:6152,10:7407,11:7336,12:8264}

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(list(B), list(B.values()), marker="o", ms=4, color="#2f6db5", label="B 欄")
ax.plot(list(C), list(C.values()), marker="s", ms=4, color="#f0884a", label="C 欄")

# 數值標籤
for d, v in B.items():
    ax.annotate(f"{v}", (d, v), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=6.5, color="#2f6db5")
for d, v in C.items():
    ax.annotate(f"{v}", (d, v), textcoords="offset points", xytext=(0, -12),
                ha="center", fontsize=6.5, color="#c4622d")

ax.set_title("每日數值比較（資料來源：你的試算表 2026 分頁）", fontsize=15)
ax.set_xlabel("日"); ax.set_ylabel("旅客量（人）")
ax.set_xticks(range(1, 32))
ax.legend(fontsize=12)
ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("flight_analysis/output/旅客量每日比較.png", dpi=140, bbox_inches="tight")
print("已輸出 flight_analysis/output/旅客量每日比較.png")
print(f"B欄 合計={sum(B.values()):,}（日2~31，未含日1）")
print(f"C欄 合計={sum(C.values()):,}（日2~12）")
