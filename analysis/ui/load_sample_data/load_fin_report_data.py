import json
import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
from scripts_stock.utils.datetime.date_function import date_today_yesterday

def load_fin_report_data(stock_index=600900):
    sql_str = f"""
        select distinct
        SECURITY_CODE as stock_index,
        SECURITY_NAME_ABBR as stock_name,
        BASIC_EPS, --每股收益
        TOTAL_OPERATE_INCOME, --营业总收入
        PARENT_NETPROFIT, --净利润
        XSMLL, --销售毛利率
        WEIGHTAVG_ROE, --净资产收益率
        BPS, -- 每股净资产
        MGJYXJJE, --每股经营现金流
        substr(UPDATE_DATE, 1, 10) as update_date,
        substr(REPORTDATE, 1, 10) as report_date
        from r_t_fin_report where SECURITY_CODE={stock_index}
        --order by UPDATE_DATE
    """
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(
        sql_str, conn).round(3).drop_duplicates().sort_values("report_date")
    #print(df1)
    return df1

def tes():
    df1 = load_fin_report_data(stock_index=600900)
    print(df1)
    print(df1.columns)

    ['BASIC_EPS', 'TOTAL_OPERATE_INCOME',
    'PARENT_NETPROFIT', 'XSMLL', 'WEIGHTAVG_ROE', 'BPS', 'MGJYXJJE']
