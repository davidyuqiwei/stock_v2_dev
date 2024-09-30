# -*- coding: utf-8 -*-
# @Time : 2023/8/21 10:52
# @Author: Davidyu
# @FileName: owner_data_sina.py


from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.open_url import get_html_table
from scripts_stock.utils.parse_data import parse_chigu_table_sina
from scripts_stock.utils.logging_set import *

import os
import pandas as pd
from scripts_stock.data_base.insert_into_db import insert_df_to_db


class DownloadSinaOwner:
    def __init__(self):
        self.owner_sina_comb_file = os.path.join(
            ProjectDir.parse_data_dir_owner_sina, "owner_sina_combine" + ".csv"
        )
        self.out_df = ""
        self.save_tmp_data_dir = ProjectDir.download_data_dir_owner_sina
        # self.save_combine_data = ProjectDir.parse_data_dir_owner_sina

    def download_owner_sina(self, owner_name, url):
        table, _ = get_html_table(url)
        df_out = parse_chigu_table_sina(table)
        # clean data
        df_out.columns = [
            "stock_name",
            "hold_num",
            "hold_ratio",
            "stock_type",
            "update_date",
        ]
        # at least one data is numeric in the rows
        df_out1 = df_out[df_out["hold_num"].map(DataFrameProcess.is_numeric)]
        df_out1["owner_name"] = owner_name
        # print(df_out1)
        save_name = os.path.join(self.save_tmp_data_dir, owner_name + ".csv")
        df_out1.drop_duplicates().to_csv(save_name, index=False, encoding="utf-8-sig")
        if df_out1.shape[0] == 0:
            TNLog().error("data row is 0")
            TNLog().error(owner_name)
        print("============= save data to {} =================".format(save_name))

    def main_run_download_owner_sina(self):
        from scripts_stock.download_data.owner_sina.owner_url_list_sina import DataURLSina
        owner_list = DataURLSina().sina_owner_list()

        for owner_name, url in owner_list:
            print(f"========= start {owner_name}=============")
            self.download_owner_sina(owner_name, url)
            time.sleep(10)


    """
    combine save save data to DB
    """
    def combine_owner_sina_data(self):
        df_merge =  DataFrameProcess.combine_all_dataframe_in_dir(self.save_tmp_data_dir)
        df_merge.drop_duplicates().to_csv(
            self.owner_sina_comb_file, index=False, encoding="utf-8-sig"
        )
        return self
        # self.out_df = df_merge
        # return df_merge
    
    def insert_index_data2db(self):
        insert_df_to_db(self.owner_sina_comb_file,"prd_t_owner_sina")
        TNLog().info("==== +++++  save owner sina data into DB ++++++ =====")


def run_download_owner_sina():
    try:
        DownloadSinaOwner().main_run_download_owner_sina()
    except:
        TNLog().error("=== download owner sina bug =====")
        pass
    DownloadSinaOwner().combine_owner_sina_data().insert_index_data2db()
    #DownloadSinaOwner().insert_index_data2db()


if __name__ == "__main__":
    print("test")
    run_download_owner_sina()
    #owner_sina_data_insert_to_db()
