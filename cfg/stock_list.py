# -*- coding: utf-8 -*-            
# @Time : 2023/8/22 16:04
# @Author: Davidyu
# @FileName: stock_list.py

import pandas as pd

from scripts_stock.cfg.set_dir import ProjectDir
import os 

class StockList:

    @staticmethod
    def all_stock():
        # 所有股票
        stock_list_data = pd.read_excel(os.path.join(ProjectDir.data_dir,"raw_data/all_stock_qianlong_20230823_v2.xls"))
        stock_list_all = [str(x).zfill(6) for x in stock_list_data["stock_index"].tolist()]
        return stock_list_all
    
    @staticmethod
    def sz50():
        # 上证50
        shangzheng50 = pd.read_excel(os.path.join(ProjectDir.data_dir,"raw_data/shangzheng50.xls"))
        shangzheng50_list = [str(x).zfill(6) for x in shangzheng50["stock_index"].tolist()]
        return shangzheng50_list
    
    @staticmethod
    def hs300():
        hs300_df = pd.read_excel(os.path.join(ProjectDir.data_dir,"raw_data/hushen_300.xls"))
        hd300_list = [str(x).zfill(6) for x in hs300_df["stock_index"].tolist()]
        return hd300_list

    print("============ import stock list:  stock_list   ================")


if __name__ == '__main__':
    hs300 = StockList.hs300()
    print(hs300)
