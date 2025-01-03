# -*- coding: utf-8 -*-
# @Time : 2023/8/21 11:07
# @Author: Davidyu
# @FileName: data_frame_process.py

from scripts_stock.utils.logging_set import *


def contains_any(main_str, substr_list):
    return any(sub in main_str for sub in substr_list)

class DataFrameProcess:
    @staticmethod
    def is_numeric(value):
        try:
            float(value)
            return True
        except:
            return False


    # df_out.apply(lambda x: x.map(DataFrameProcess.is_numeric))

    @staticmethod
    def combine_all_dataframe_in_dir(target_dir, file_type=".csv",keywords_list=[""]):
        import os
        import pandas as pd

        file_list = os.listdir(target_dir)
        csv_list = [x for x in file_list if file_type in x]
        df_list = []
        for csv_file in csv_list:
            if contains_any(csv_file, keywords_list):
                print(csv_file)
                try:
                    file_in = os.path.join(target_dir, csv_file)
                    df1 = pd.read_csv(file_in)
                    df_list.append(df1)
                except Exception as e:
                    print("======combine dataframe error========")
                    TNLog().error(e)
                    print_exception_info()
                    TNLog().error(file_in)
                    pass
        df2 = pd.concat(df_list,sort=False).drop_duplicates()
        return df2
    

if __name__ == "__main__":
    print(1)
    # stock_download_dir = "/home/davidyu/vscode/data/download_data/fuquan"
    # df1 = DataFrameProcess.combine_all_dataframe_in_dir(stock_download_dir)
    # print(df1)
    #print(contains_any("2023_232",["32"]))