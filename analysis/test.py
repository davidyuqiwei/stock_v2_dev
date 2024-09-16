# -*- coding: utf-8 -*-            
# @Time : 2023/8/22 17:37
# @Author: Davidyu
# @FileName: test.py


import pandas as pd
from scripts_stock.cfg.set_dir import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df

stock_list_in = "600004"
fq_file_name = os.path.join(parse_data_dir, "fq_" + stock_list_in + ".csv")

df1 = pd.read_csv(fq_file_name)
df1['stock_date'] = df1["date"]
del df1["date"]
print(df1)
df2 = df_to_stock_df(df1)
print("----------------------------------------------------")
print("----------------------------------------------------")

print(df2["kdjj"])


def stock_kdj(stock, feature_list=None):
    if feature_list is None:
        feature_list = ["macdh", "cci", "rsi_6", "rsi_12", "rsi_24", "kdjk", "kdjd", "kdjj", "boll_ub", "boll_lb",
                        "macd", "macds",
                        "wr_6", "wr_10"]
    # df_kdj = stock[['kdjk','kdjd','kdjj']].reset_index()
    df_kdj = stock.reset_index()
    df_kdj['stock_index'] = stock['stock_index'].tolist()
    df_kdj['stock_date'] = df_kdj['date']
    df_kdj['stock_date'] = df_kdj['stock_date'].astype(str)
    for k in feature_list:
        df_kdj[k] = stock[k].reset_index()[k]
    return df_kdj, feature_list


a1, a2 = stock_kdj(df2)
print(a1)
