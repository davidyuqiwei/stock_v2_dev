import json
import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess

import plotly.figure_factory as ff
import numpy as np
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.utils.datetime.date_function import date_today_yesterday
from scripts_stock.data_base.insert_into_db import df_save_to_db



today_date, _, two_month_ago = date_today_yesterday(150)

start_date = two_month_ago
end_date = today_date
sql_str = f"""
   select distinct stock_index,date,
   small_order_net_inflow_amount,medium_order_net_inflow_amount,
     large_order_net_inflow_amount,
     super_large_order_net_inflow_amount
     from r_t_cash_flow_stocks 
     where date>='{start_date}' and date<='{end_date}'
        
"""
conn = CommonScript.connect_to_db("test.db")
df1 = pd.read_sql_query(sql_str, conn)
print(df1.tail(4))
print("get data")


def normalize_row(row):
    # 获取所有正数和负数
    positive_values = row[row > 0]
    negative_values = row[row < 0]

    # 计算正数和负数的总和
    sum_positive = positive_values.sum()
    sum_negative = negative_values.sum()

    # 避免除以零
    if sum_positive != 0:
        row[row > 0] = positive_values / sum_positive
    if sum_negative != 0:
        row[row < 0] = (negative_values / sum_negative)*-1

    return row


# 应用归一化函数到每一列
df_v2 = df1[["small_order_net_inflow_amount", "medium_order_net_inflow_amount",
             "large_order_net_inflow_amount", "super_large_order_net_inflow_amount"]]
df_normalized2 = df_v2.apply(normalize_row, axis=1)

df_merged = pd.merge(df1, df_normalized2, left_index=True,
                     right_index=True, suffixes=('_from_df1', '_ratio'))

df_save_to_db(input_df=df_merged,target_table="cal_t_stocks_cash_flow_ratio")
print(df_merged.round(3))
