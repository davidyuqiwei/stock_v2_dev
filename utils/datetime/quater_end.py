import calendar
from datetime import datetime, timedelta

# 定义起始年份和结束年份
start_year = 2013
end_year = 2024

# 函数来获取给定年份和季度的最后一天
def get_last_day_of_quarter(year, quarter):
    # 第一季度: 3月31日, 第二季度: 6月30日, 第三季度: 9月30日, 第四季度: 12月31日
    if quarter == 4:
        # 如果是第四季度，直接返回12月31日
        last_day = datetime(year, 12, 31)
    else:
        # 对于其他季度，找到该季度末月的第一天然后减去一天
        month = 3 * quarter  # 每个季度的最后一个月
        last_day = datetime(year, month+1, 1) - timedelta(days=1)
    
    return last_day.strftime('%Y-%m-%d')  # 返回日期字符串

def get_last_day_of_quarter_range(start_year=2013,end_year=2024):
    quater_end_list = []
    # 主循环遍历年份和季度
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):  # 一年有四个季度
            quater_end_list.append(get_last_day_of_quarter(year, quarter))
    return quater_end_list

if __name__ == "__main__":
    a1 = get_last_day_of_quarter_range()
    print(a1)