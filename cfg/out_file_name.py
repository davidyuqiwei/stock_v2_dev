# -*- coding: utf-8 -*-            
# @Time : 2023/8/23 5:12
# @Author: Davidyu
# @FileName: out_file_name.py
# from ast import main
import os
from scripts_stock.cfg.set_dir import *


class OutFileName():
    @staticmethod
    def fuquan_data_name(parse_data_dir, stock_list_in):
        fq_file_name = os.path.join(parse_data_dir, "fq_" + stock_list_in + ".csv")
        return fq_file_name



if __name__ == "__main__":
    save_dir = ProjectDir.download_data_dir_fuquan
    stock_list_in = "601398"
    save_name = OutFileName.fuquan_data_name(save_dir, stock_list_in)
    print(save_name)
