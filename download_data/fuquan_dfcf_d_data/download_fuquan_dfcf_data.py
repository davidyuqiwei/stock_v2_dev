# -*- coding: utf-8 -*-
# @Time : 2023/8/22 16:01
# @Author: Davidyu
# @FileName: fuquan_dfcf_sche.py


from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.download_data.fuquan_dfcf_d_data.fuquan_dfcf import *
from scripts_stock.parse_download_data.fuquan_dfcf_parse import parse_fuquan_data
from scripts_stock.utils.logging_set import *
from scripts_stock.utils.data_frame_process import DataFrameProcess

def download_fuquan_schedule(stock_list_fq, save_dir):
    """
    mv hushen_300.xls hushen_300.xls.bak 
    mv all_stock_qianlong_20240908.xls hushen_300.xls
    """
    for stock_list_in in stock_list_fq:
        try:
            print(stock_list_in)
            save_data_dir_fq = download_fuquan_data(stock_list_in, save_dir)
            df_fq = parse_fuquan_data(save_data_dir_fq)
            df_fq["stock_index"] = stock_list_in
            fq_file_name = OutFileName.fuquan_data_name(save_dir, stock_list_in)
            df_fq.to_csv(fq_file_name, index=False)
            time.sleep(10)
        except Exception as e:
            TNLog().error("cannot download fuquan data:" + stock_list_in)
            print("============ the error is ==========")
            print(e)
            print("====================================")
            pass


def combine_fuquan_data(stock_download_dir, all_dir):
    import pandas as pd

    df2 = DataFrameProcess.combine_all_dataframe_in_dir(stock_download_dir)
    fq_file_name = OutFileName.fuquan_data_name(all_dir, "all")
    df2.to_csv(fq_file_name, index=False)


def main_download_fuquan_test(StockList,ProjectDir):
    download_fuquan_schedule(
            StockList.hs300()[0:5], ProjectDir.download_data_dir_fuquan
        )
    TNLog().info("=== Finish download test fuquan DFCF data =====")


def main_download_fuquan_all(StockList,ProjectDir):
    download_fuquan_schedule(StockList.hs300(), ProjectDir.download_data_dir_fuquan)
    """
    save combine data to csv
    """
    TNLog().info("=== Start combine fuquan data =====")
    combine_fuquan_data(
        ProjectDir.download_data_dir_fuquan, ProjectDir.parse_data_dir_fuquan
    )
    TNLog().info(f"==={ProjectDir.parse_data_dir_fuquan} ===")


def run_download_fuquan_schedule(download_type="ALL"):
    """
    download HS 300 data
    """
    from scripts_stock.cfg.stock_list import StockList
    try:
        TNLog().info("=== Start download fuquan data =====")
        if download_type == "test":   
           main_download_fuquan_test(StockList,ProjectDir)
        else:
           main_download_fuquan_all(StockList,ProjectDir)
    except:
        TNLog().error("=== download dfcf data bug =====")
        pass
        

if __name__ == "__main__":
    from scripts_stock.cfg.set_dir import ProjectDir
    from scripts_stock.cfg.stock_list import StockList
    from scripts_stock.data_base.insert_into_db import fuquan_data_insert_to_db
    
    run_download_fuquan_schedule("test")
    # fuquan_data_insert_to_db()
