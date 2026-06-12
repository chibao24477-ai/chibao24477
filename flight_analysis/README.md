# 航班月報分析範本

依需求產出三項：環比(本月vs上月)、年同期(本月vs去年同月)、趨勢圖。

## 檔案
- `make_sample_data.py`：產生模擬資料示範用（正式使用可忽略）
- `flights.csv`：資料來源，欄位 `date, flight_no, passengers, amount`（每列=某天某航班一次起飛）
- `analyze.py`：產出文字報表 + `output/` 內三張圖
- `output/`：圖表輸出

## 使用
1. 把 `flights.csv` 換成真實資料（欄位不變；無旅客數則留空，載客率/客單價/量價拆解會略過）
2. 編輯 `analyze.py` 上方 `CUR/PREV/YOY` 設定本月、上月、去年同月
3. `python3 flight_analysis/analyze.py`

## 產出
- 要求1：本月 vs 上月 — 航班數/旅客量/金額 差異表 + 原因
- 要求2：本月 vs 去年同月 — 同上 + YoY 原因
- 要求3：①月份比較長條圖 ②每日金額走勢折線 ③金額差異量價拆解瀑布圖
