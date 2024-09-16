# -*- coding: utf-8 -*-            
# @Time : 2023/8/29 22:41
# @Author: Davidyu
# @FileName: owner_sina.py
from scripts_stock.cfg.set_dir import *
import pandas as pd

project_dir = ProjectDir()
df1 = pd.read_csv(os.path.join(project_dir.download_data_dir,"owner_sina","sina_owner_abudabi.csv"),encoding="utf-8-sig")
df2 = df1.groupby("stock_name").agg({'hold_num': [ 'min', 'max']})
print(df2.reset_index())