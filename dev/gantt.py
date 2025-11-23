import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# --- 配色定義 (已修改以增加工作日與假日的對比度) ---
catCream = "#FFFFFF"      # 工作日背景 (更亮的白色)
catOrange = "#F4A261"      # 可用於工作條高亮
catBrown = "#5A3E36"      # 工作條主色/文字主色
catGrayBase = "#AAAAAA"    # X軸文字顏色
catGrayHover = "#C0C0C0"   # 網格線顏色
catWeekend = "#F0E0D0"     # 假日背景色 (對比度更高的顏色)

# --- 額外假日定義 ---
# 設定您希望被視為假日的日期 (格式: "MM/DD")
custom_holidays_str = ["11/21"]
# 將字串轉換為 datetime.date 物件，方便比較
custom_holidays = [datetime.strptime("2025/" + d, "%Y/%m/%d").date() for d in custom_holidays_str]


# Input data (不變)
data = [
    ["10/24", "14:07", "15:35"],
    ["10/24", "17:36", "20:10"],
    ["10/24", "22:13", "23:20"],
    ["10/25", "01:15", "04:04"],
    ["10/25", "11:12", "12:00"],
    ["10/25", "15:00", "15:30"],
    ["10/25", "16:30", "18:10"],
    ["10/25", "18:20", "18:37"],
    ["10/25", "20:55", "22:12"],
    ["10/26", "00:54", "03:06"],
    ["10/26", "11:54", "12:14"],
    ["10/26", "20:08", "21:14"],
    ["10/26", "23:30", "00:00"],
    ["10/27", "00:00", "01:08"],
    ["10/28", "09:00", "10:00"],
    ["11/2", "03:45", "06:35"],
    ["11/2", "14:25", "14:56"],
    ["11/2", "17:47", "19:42"],
    ["11/2", "22:00", "22:41"],
    ["11/3", "01:09", "03:48"],
    ["11/5", "03:00", "03:40"],
    ["11/6", "03:26", "05:00"],
    ["11/8", "22:23", "00:00"],
    ["11/9", "00:00", "00:25"],
    ["11/9", "03:30", "05:58"],
    ["11/9", "16:10", "16:51"],
    ["11/9", "17:20", "18:10"],
    ["11/9", "21:10", "21:40"],
    ["11/9", "22:30", "23:50"],
    ["11/10", "02:14", "03:57"],
    ["11/11", "02:56", "04:05"],
    ["11/12", "20:26", "22:36"],
    ["11/13", "02:30", "04:14"],
    ["11/15", "15:00", "16:21"],
    ["11/15", "18:04", "18:19"],
    ["11/15", "21:41", "21:55"],
    ["11/16", "01:43", "14:12"],
    ["11/16", "13:21", "13:39"],
    ["11/16", "14:10", "15:07"],
    ["11/16", "17:25", "18:54"],
    ["11/16", "23:40", "00:00"],
    ["11/17", "00:00", "02:15"],
    ["11/17", "21:20", "22:07"],
    ["11/18", "18:49", "20:00"],
    ["11/18", "22:40", "23:30"],
    ["11/20", "00:31", "06:01"],
    ["11/20", "18:00", "20:47"],
    ["11/20", "21:17", "00:00"],
    ["11/21", "00:00", "03:00"],
    ["11/21", "10:00", "12:00"],
    ["11/21", "13:00", "19:41"]
]

df = pd.DataFrame(data, columns=["date", "start", "end"])

# Convert times to float hours (不變)
def to_hour(t):
    dt = datetime.strptime(t, "%H:%M")
    return dt.hour + dt.minute / 60

df["start_h"] = df["start"].apply(to_hour)
df["end_h"] = df["end"].apply(to_hour)

# Convert date strings to datetime (year 2025) (不變)
df["date_dt"] = pd.to_datetime("2025/" + df["date"], format="%Y/%m/%d")

# Continuous date range (不變)
all_dates = pd.date_range(df["date_dt"].min(), df["date_dt"].max(), freq='D')

# Plot
plt.figure(figsize=(14, len(all_dates) * 0.45))
ax = plt.gca()

# --- 背景區分工作日/週末/自定義假日 (已修改) ---
for i, d in enumerate(all_dates):
    is_weekend = d.weekday() >= 5  # 0=Mon, 6=Sun
    is_custom_holiday = d.date() in custom_holidays # 檢查是否為自定義假日

    if is_weekend or is_custom_holiday:
        bgcolor = catWeekend
    else:
        bgcolor = catCream
        
    ax.barh(i, 24, left=0, height=0.6, color=bgcolor, edgecolor="none")

# 工作時間條 (不變)
for i, d in enumerate(all_dates):
    day_data = df[df["date_dt"] == d]
    for _, row in day_data.iterrows():
        start = row["start_h"]
        end = row["end_h"]
        if end == 0:
            end = 24
        plt.barh(i, end - start, left=start, height=0.6, color=catBrown)

# --- Formatting (Y軸對齊已修改) ---
# 使用 ha='right' (水平對齊右邊) 參數使文字對齊
plt.yticks(
    range(len(all_dates)), 
    [d.strftime("%m/%d (%a)") for d in all_dates], 
    color=catBrown, 
    fontsize=10,
    ha='right' # 使所有 Y 軸標籤右對齊，解決排版混亂問題
) 

plt.xticks(range(0, 25, 2), color=catGrayBase)
plt.xlabel("Hour of Day (0-24)", color=catBrown)
plt.title("Daily Work Time Visualization (24h Format)", color=catBrown)
plt.xlim(0, 24)
plt.grid(axis="x", linestyle='--', color=catGrayHover, alpha=0.7)

# 顯示上方 X 軸 (不變)
ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xticks(range(0, 25, 2))
ax_top.set_xticklabels(range(0, 25, 2), color=catGrayBase)

plt.gca().invert_yaxis()  # earliest date on top
plt.tight_layout()

# 儲存為 PNG 檔案，並使用 bbox_inches='tight' 確保圖表完整
plt.savefig("work_time_gantt.png", bbox_inches='tight', dpi=300) 

plt.show() # 照常顯示圖表