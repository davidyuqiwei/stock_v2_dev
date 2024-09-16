# -*- coding: utf-8 -*-            
# @Time : 2023/8/22 15:58
# @Author: Davidyu
# @FileName: fuquan_dfcf_parse.py

from scripts_stock.cfg.set_dir import *
from scripts_stock.utils.json_to_df import read_txt_file
import re
import pandas as pd


def parse_fuquan_data(data_dir):
    # data_name = "fuquan_600006.txt"
    # test_file = os.path.join(download_data_dir, data_name)

    df1 = read_txt_file(data_dir)
    # print(df1)

    dta = re.findall('klines":\\[(.*)]', df1)
    dta1 = dta[0].split("\",")
    df_list = []

    for k in dta1:
        dta2 = k.replace("\"", "")
        aa = dta2.split(",")
        df_list.append(aa)
    df_out = pd.DataFrame(df_list)
    df_out1 = df_out.iloc[:, 0:5]
    df_out1.columns = ["date", "open", "close","high","low"]
    return df_out1

#
# data_name = "fuquan_600006.txt"
# test_file = os.path.join(download_data_dir, data_name)
#
# df1 = read_txt_file(test_file)
# #print(df1)
#
# dta = re.findall('klines":\\[(.*)]', df1)
# dta1 = dta[0].split("\",")
# df_list = []
#
# for k in dta1:
#     dta2 = k.replace("\"","")
#     aa = dta2.split(",")
#     df_list.append(aa)
# df_out = pd.DataFrame(df_list)
# print(df_out)
#


# dta1 = dta[0]
# # print(dta1)
# df = pd.read_json(dta1, encoding="utf-8", orient='records')
# df.to_csv(os.path.join(parse_data_dir, "all_owner_data.csv"), index=0)
