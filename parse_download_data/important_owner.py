# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 21:19
# @Author: Davidyu
# @FileName: important_owner.py
import re

from scripts_stock.cfg.set_dir import *
from scripts_stock.utils.clean_data import CleanData
from scripts_stock.utils.json_to_df import read_txt_file
import pandas as pd
import numpy as np

from scripts_stock.utils.parse_data import parse_data_to_df


# def clean_data(save_data="parse_data.csv"):
#
#     df = pd.read_csv(os.path.join(parse_data_dir,save_data))
#     print(os.path.join(parse_data_dir,save_data))
#     xx = df1["SEAB_JOIN"]
#     #print(df.columns)
#     return df

def clean_data_str(input_str):
    x_clean = [x.split("|") for x in input_str.split(",")]
    return x_clean


def df_split_flat(df1):
    split_col = df1["SEAB_JOIN"]
    d_list = []
    for i in range(0, len(split_col)):
        add_str = clean_data_str(split_col[i])
        add_str_df = pd.DataFrame(add_str)
        add_str_df.columns = ["stock_index", "stock_name"]
        new_df = pd.DataFrame(np.repeat(df1.iloc[i:(i + 1), :].values, len(add_str), axis=0))
        # print(new_df)
        new_df.columns = df1.columns
        new_df["stock_index"] = add_str_df["stock_index"]
        new_df["stock_name"] = add_str_df["stock_name"]
        d_list.append(new_df)
    df2 = pd.concat(d_list)
    return df2


#
# def parse_data_to_df_history(file_in):
#     """
#     *** Need to update ***
#     :param file_in:
#     :return:
#     """
#     for i in range(0,5):
#         df1 = read_txt_file(file_in)
#         # print(df1)
#         dta = re.findall('data":(.*)\\,"count', df1)
#         dta1 = dta[0]
#         # print(dta1)
#         df = pd.read_json(dta1, encoding="utf-8", orient='records')
#         df.to_csv(os.path.join(parse_data_dir, "all_owner_data.csv"),index=0)
#         return df

def tt():
    print("2323")

if __name__ == '__main__':
    test_file = "../../data/download_sample_data/important_owner.txt"
    _, data_path = parse_data_to_df(test_file)
    df1 = pd.read_csv(data_path)
    df2 = df_split_flat(df1)
    df3 = df2[['COOPERATION_HOLDER_MARK', 'END_DATE', 'HOLDER_NAME', 'HOLDER_TYPE',
               'HOLDNUM_CHANGE_TYPE', 'STATISTICS_TIMES', 'stock_index', 'stock_name']]
    df3.to_csv("../../data/parse_data/important_owner.csv", index=0)
