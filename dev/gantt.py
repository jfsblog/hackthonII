import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm # 導入字型管理器

# --- 字型設定 (假設 font.ttf 存在於當前目錄或系統可存取路徑) ---
# **請務必確認 font.ttf 檔案可被程式存取**
font_path = 'dev/font.ttf'
try:
    # 嘗試載入自定義字型
    fm.fontManager.addfont(font_path)
    # 取得字型名稱 (通常是檔案名稱，但 Matplotlib 內部會解析實際名稱)
    prop = fm.FontProperties(fname=font_path)
    custom_font_name = prop.get_name()
    plt.rcParams['font.sans-serif'] = [custom_font_name] + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False # 解決負號亂碼問題
    print(f"成功載入字型: {custom_font_name}")
except FileNotFoundError:
    # 如果找不到字型，仍會使用預設字型繪圖，但中文可能顯示為方塊
    print(f"警告：找不到字型檔案 {font_path}。圖表可能無法正確顯示中文字體。")
    custom_font_name = None # 確保後續中文可以被處理

# --- 配色定義 ---
catOrange = "#F4A261"      
catBrown = "#5A3E36"      # 工作條主色/文字主色
catGrayBase = "#AAAAAA"    # X軸文字顏色
catGrayHover = "#C0C0C0"   # 網格線顏色
catWorkHourHighlight = "#BCCAE0" # 平日排定工時的低飽和藍色
transparent_weekend_color = "#F0E0D0" # 假日半透明背景色


# --- 額外假日定義 ---
custom_holidays_str = ["10/24","11/21"]
custom_holidays = [datetime.strptime("2025/" + d, "%Y/%m/%d").date() for d in custom_holidays_str]


# Input data (不變)
data = [
    ["10/24", "14:07", "15:35"], ["10/24", "17:36", "20:10"], ["10/24", "22:13", "23:20"],
    ["10/25", "01:15", "04:04"], ["10/25", "11:12", "12:00"], ["10/25", "15:00", "15:30"],
    ["10/25", "16:30", "18:10"], ["10/25", "18:20", "18:37"], ["10/25", "20:55", "22:12"],
    ["10/26", "00:54", "03:06"], ["10/26", "11:54", "12:14"], ["10/26", "20:08", "21:14"],
    ["10/26", "23:30", "00:00"], ["10/27", "00:00", "01:08"], ["10/28", "09:00", "10:00"],
    ["11/2", "03:45", "06:35"], ["11/2", "14:25", "14:56"], ["11/2", "17:47", "19:42"],
    ["11/2", "22:00", "22:41"], ["11/3", "01:09", "03:48"], ["11/5", "03:00", "03:40"],
    ["11/6", "03:26", "05:00"], ["11/8", "22:23", "00:00"], ["11/9", "00:00", "00:25"],
    ["11/9", "03:30", "05:58"], ["11/9", "16:10", "16:51"], ["11/9", "17:20", "18:10"],
    ["11/9", "21:10", "21:40"], ["11/9", "22:30", "23:50"], ["11/10", "02:14", "03:57"],
    ["11/11", "02:56", "04:05"], ["11/12", "20:26", "22:36"], ["11/13", "02:30", "04:14"],
    ["11/15", "15:00", "16:21"], ["11/15", "18:04", "18:19"], ["11/15", "21:41", "21:55"],
    ["11/16", "01:43", "14:12"], ["11/16", "13:21", "13:39"], ["11/16", "14:10", "15:07"],
    ["11/16", "17:25", "18:54"], ["11/16", "23:40", "00:00"], ["11/17", "00:00", "02:15"],
    ["11/17", "21:20", "22:07"], ["11/18", "18:49", "20:00"], ["11/18", "22:40", "23:30"],
    ["11/20", "00:31", "06:01"], ["11/20", "18:00", "20:47"], ["11/20", "21:17", "00:00"],
    ["11/21", "00:00", "03:00"], ["11/21", "10:00", "12:00"], ["11/21", "13:00", "19:41"]
]

df = pd.DataFrame(data, columns=["date", "start", "end"])
def to_hour(t):
    dt = datetime.strptime(t, "%H:%M")
    return dt.hour + dt.minute / 60
df["start_h"] = df["start"].apply(to_hour)
df["end_h"] = df["end"].apply(to_hour)
df["date_dt"] = pd.to_datetime("2025/" + df["date"], format="%Y/%m/%d")
all_dates = pd.date_range(df["date_dt"].min(), df["date_dt"].max(), freq='D')

# Plot - 設定透明背景
plt.figure(figsize=(14, len(all_dates) * 0.45), facecolor='None', edgecolor='None')
ax = plt.gca()
ax.set_facecolor('None') # 確保座標軸區域背景也是透明

# --- 背景區分工作日/週末/自定義假日 及 標註工作時間 ---
for i, d in enumerate(all_dates):
    is_weekend = d.weekday() >= 5  # 0=Mon, 6=Sun
    is_custom_holiday = d.date() in custom_holidays # 檢查是否為自定義假日

    # 1. 繪製全天背景 - 僅繪製假日，平日完全留白(透明)
    if is_weekend or is_custom_holiday:
        ax.barh(i, 24, left=0, height=0.6, color=transparent_weekend_color, edgecolor="none", alpha=0.5)
        
    
    # 2. 如果是非假日 (工作日)，則標註工作時間 (10:00~18:00)
    if not (is_weekend or is_custom_holiday):
        work_start_h = 10
        work_end_h = 18
        work_duration = work_end_h - work_start_h
        ax.barh(i, work_duration, left=work_start_h, height=0.6, 
                color=catWorkHourHighlight, edgecolor="none", alpha=0.5) 

# 工作時間條 (不變)
for i, d in enumerate(all_dates):
    day_data = df[df["date_dt"] == d]
    for _, row in day_data.iterrows():
        start = row["start_h"]
        end = row["end_h"]
        if end == 0:
            end = 24
        plt.barh(i, end - start, left=start, height=0.6, color=catBrown)

# --- Formatting ---
# Y 軸標籤 (日期+星期)
plt.yticks(
    range(len(all_dates)), 
    [d.strftime("%m/%d (%a)") for d in all_dates], 
    color=catBrown, 
    fontsize=10,
    ha='right'
) 

# X 軸標籤
plt.xticks(range(0, 25, 2), color=catGrayBase)
# X 軸文字標籤 (英文改中文)
plt.xlabel("一天中的小時 (0-24)", color=catBrown)
# 圖表標題 (英文改中文)
plt.title("每日工時甘特圖 (24小時格式)", color=catBrown)
plt.xlim(0, 24)

# 網格線設定不變
plt.grid(axis="x", linestyle='--', color=catGrayHover, alpha=0.7)

# 顯示上方 X 軸 (不變)
ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xticks(range(0, 25, 2))
ax_top.set_xticklabels(range(0, 25, 2), color=catGrayBase)


# --- 圖例 ---
legend_handles = [
    mpatches.Patch(color='None', label='平日'),
    mpatches.Patch(color=transparent_weekend_color, alpha=0.5, label='放假日 (週末/特定日期)'),
    mpatches.Patch(color=catWorkHourHighlight, alpha=0.5, label='平日排定工時 (10:00-18:00)'),
    mpatches.Patch(color=catBrown, label='實際紀錄工時')
]

plt.legend(
    handles=legend_handles, 
    loc='upper center', 
    bbox_to_anchor=(0.5, -0.1), 
    ncol=2, 
    frameon=False,
    fontsize=10
)

plt.subplots_adjust(bottom=0.15) 

plt.gca().invert_yaxis()  
plt.tight_layout()

# 儲存為 PNG 檔案，設置 transparent=True 確保背景透明
plt.savefig("work_time_gantt.png", bbox_inches='tight', dpi=300, transparent=True) 

plt.show()