import pandas as pd

def get_quarter_ends(year=None):
    """获取指定年份每个季度的最后一天，并输出为字符串格式。
    如果没有指定年份，则默认为当前年份。
    """
    if year is None:
        year = pd.Timestamp.now().year
    
    # 定义每个季度最后一天的日期
    quarter_ends = [
        pd.Timestamp(f'{year}-03-31'),
        pd.Timestamp(f'{year}-06-30'),
        pd.Timestamp(f'{year}-09-30'),
        pd.Timestamp(f'{year}-12-31')
    ]
    
    # 将日期格式化为字符串
    formatted_dates = [date.strftime('%Y-%m-%d') for date in quarter_ends]
    
    return formatted_dates

# # 获取当前年份每个季度的最后一天，并输出为字符串格式
# current_year_quarter_ends = get_quarter_ends()
# print("当前年份每个季度的最后一天:", current_year_quarter_ends)

# # 获取指定年份每个季度的最后一天，并输出为字符串格式
# specified_year_quarter_ends = get_quarter_ends(2023)
# print("2023年每个季度的最后一天:", specified_year_quarter_ends)


class DateRangeCalculator:
    def __init__(self, start_date=None, end_date=None):
        if start_date is None:
            self.start_date = pd.Timestamp.today()
        else:
            self.start_date = pd.Timestamp(start_date)
        
        if end_date is None:
            self.end_date = pd.Timestamp.today()
        else:
            self.end_date = pd.Timestamp(end_date)
    
    def get_month_start_end(self, date=None):
        """获取指定月份的月初和月末日期。
        如果未指定日期，则使用实例的开始日期。
        """
        if date is None:
            date = self.start_date
        
        month_start = date.normalize()  # 获取当月的第一天
        month_end = month_start + pd.offsets.MonthEnd(0)  # 获取当月的最后一天
        
        return month_start, month_end
    
    def get_quarter_start_end(self, date=None):
        """获取指定季度的季度初和季度末日期。
        如果未指定日期，则使用实例的开始日期。
        """
        if date is None:
            date = self.start_date
        
        quarter_start = date.to_period('Q').start_time  # 获取当季的第一天
        quarter_end = date.to_period('Q').end_time  # 获取当季的最后一天
        
        return quarter_start, quarter_end
    
    def generate_monthly_ranges(self):
        """生成每个月的月初和月末日期的列表。
        """
        monthly_ranges = []
        current_date = self.start_date
        while current_date <= self.end_date:
            month_start, month_end = self.get_month_start_end(current_date)
            monthly_ranges.append((month_start, month_end))
            current_date = month_end + pd.offsets.Day(1)
        return monthly_ranges
    
    def generate_quarterly_ranges(self):
        """生成每个季度的季度初和季度末日期的列表。
        """
        quarterly_ranges = []
        current_date = self.start_date
        while current_date <= self.end_date:
            quarter_start, quarter_end = self.get_quarter_start_end(current_date)
            quarterly_ranges.append((quarter_start, quarter_end))
            current_date = quarter_end + pd.offsets.Day(1)
        return quarterly_ranges


def get_years_before_date(before=2):
    from datetime import datetime, timedelta
    # 获取当前日期
    now = datetime.now()
    # 计算两年前的日期
    two_years_ago = now - timedelta(days=365*before)
    # 输出两年前的日期
    return two_years_ago.strftime('%Y-%m-%d')

# 示例用法
if __name__ == "__main__":
    # 创建一个 DateRangeCalculator 实例
    calculator = DateRangeCalculator(start_date='2023-01-01', end_date='2023-12-31')
    
    # 获取指定日期的月初和月末
    print("Month Start and End:", calculator.get_month_start_end(pd.Timestamp('2023-01-15')))
    
    # 获取指定日期的季度初和季度末
    print("Quarter Start and End:", calculator.get_quarter_start_end(pd.Timestamp('2023-02-15')))
    
    # 生成每月的范围
    print("Monthly Ranges:", calculator.generate_monthly_ranges())
    
    # 生成每个季度的范围
    print("Quarterly Ranges:", calculator.generate_quarterly_ranges())