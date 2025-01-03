from datetime import datetime, timedelta


def date_today_yesterday(diff_days=30):
    # 获取今天的日期
    today = datetime.now().date()

    # 计算昨天的日期
    yesterday = today - timedelta(days=1)
    define_days = today - timedelta(days=diff_days)
    # 将日期对象转换成字符串，指定格式
    format_str = '%Y-%m-%d'  # 格式化字符串，可以根据需要调整

    today_str = today.strftime(format_str)
    yesterday_str = yesterday.strftime(format_str)
    define_days_str = define_days.strftime(format_str)
    # print(f"今天的日期是: {today_str}")
    # print(f"昨天的日期是: {yesterday_str}")
    return today_str, yesterday_str, define_days_str


if __name__ == "__main__":
    a1, a2,_ = date_today_yesterday()
    print(a1)
    print(a2)