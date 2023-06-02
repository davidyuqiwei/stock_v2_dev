# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:00
# @Author: Davidyu
# @FileName: parse_data.py

from scripts_stock.utils.json_to_df import read_txt_file
import re
import pandas as pd
import os

from scripts_stock.cfg.set_dir import *


def parse_data_to_df(file_in,save_data="parse_data.csv"):
    df1 = read_txt_file(file_in)
    # print(df1)
    dta = re.findall('data":(.*)\\,"count', df1)
    dta1 = dta[0]
    # print(dta1)
    df = pd.read_json(dta1, encoding="utf-8", orient='records')
    final_data_path = os.path.join(parse_data_dir, save_data)
    df.to_csv(os.path.join(parse_data_dir,save_data),index=0,encoding="utf_8_sig")
    print(df.columns)
    return df,final_data_path
