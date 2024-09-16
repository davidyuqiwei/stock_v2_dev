# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:00
# @Author: Davidyu
# @FileName: parse_data.py

from scripts_stock.utils.json_to_df import read_txt_file
import re
import pandas as pd
import os

from scripts_stock.cfg.set_dir import *
from scripts_stock.utils.string_process import StringProcess


def parse_data_to_df(file_in, project_dir, save_data="parse_data.csv"):
    df1 = read_txt_file(file_in)
    # print(df1)
    dta = re.findall('data":(.*)\\,"count', df1)
    dta1 = dta[0]
    # print(dta1)
    df = pd.read_json(dta1, encoding="utf-8", orient='records')
    final_data_path = os.path.join(project_dir.parse_data_dir, save_data)
    df.to_csv(os.path.join(project_dir.parse_data_dir, save_data), index=0, encoding="utf_8_sig")
    print(df.columns)
    return df, final_data_path


def parse_chigu_table_sina(table_in):
    # 股票简称
    # 持股数量(股)
    # 持股比例( %)
    # 股本性质
    # 截止日期
    table_in_tr = table_in.find_all('tr')
    data_list = []
    for kk in table_in_tr:

        kk_div = [x.get_text() for x in kk.find_all("div")]
        kk_div[0] = kk_div[0].split("\t")[0]
        if len(kk_div) == 5:
            kk_div_v2 = [StringProcess.parse_latin(x) for x in kk_div]
            data_list.append(kk_div_v2)
    df_out = pd.DataFrame(data_list)
    return df_out
