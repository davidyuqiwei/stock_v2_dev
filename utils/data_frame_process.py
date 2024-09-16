# -*- coding: utf-8 -*-
# @Time : 2023/8/21 11:07
# @Author: Davidyu
# @FileName: data_frame_process.py


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
    def combine_all_dataframe_in_dir(target_dir, file_type=".csv"):
        import os
        import pandas as pd

        file_list = os.listdir(target_dir)
        csv_list = [x for x in file_list if file_type in x]
        df_list = []
        for csv_file in csv_list:
            df1 = pd.read_csv(os.path.join(target_dir, csv_file))
            df_list.append(df1)
        df2 = pd.concat(df_list)
        return df2
