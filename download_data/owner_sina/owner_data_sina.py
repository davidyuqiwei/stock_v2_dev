# -*- coding: utf-8 -*-
# @Time : 2023/8/21 10:52
# @Author: Davidyu
# @FileName: owner_data_sina.py


from scripts_stock.utils.connect_db import DBprocess
from scripts_stock.utils.data_frame_process import DataFrameProcess
from scripts_stock.utils.open_url import get_html_table
from scripts_stock.utils.parse_data import parse_chigu_table_sina
from scripts_stock.utils.logging_set import *

import os
import pandas as pd


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
        from scripts_stock.cfg.owner_url_list_sina import DataURLSina

        data_url_sina = DataURLSina()
        owner_list = [
            data_url_sina.owner_abdb(),
            data_url_sina.owner_shebao102(),
            data_url_sina.owner_shebao406(),
            data_url_sina.owner_hkjiesuan(),
        ]
        for owner_name, url in owner_list:
            self.download_owner_sina(owner_name, url)
            time.sleep(10)

    def combine_owner_sina_data(self):
        df_merge =  DataFrameProcess.combine_all_dataframe_in_dir(self.save_tmp_data_dir,"sina_owner")
        df_merge.drop_duplicates().to_csv(
            self.owner_sina_comb_file, index=False, encoding="utf-8-sig"
        )
        self.out_df = df_merge
        return df_merge

    # def insert_to_db(self,target_db="test.db"):
    #     df1 = pd.read_csv(self.owner_sina_comb_file)
    #     conn = connect_db( os.path.join(ProjectDir.database_dir,target_db))
    #     table_name = "prd_t_owner_sina"
    #     df1.to_sql(table_name,conn,if_exists='replace',index=False)
    #     print(f"=============== insert to {target_db}.{table_name} ====================")


def run_download_owner_sina():
    try:
        DownloadSinaOwner().main_run_download_owner_sina()
        DownloadSinaOwner().combine_owner_sina_data()
    except:
        TNLog().error("=== download owner sina bug =====")
        pass
    # owner_sina_comb_df = DownloadSinaOwner().combine_owner_sina_data()
    # DBprocess.insert_to_db(owner_sina_comb_df,target_db="test.db")


if __name__ == "__main__":
    print("test")
    # main_run_owner_sina()
    # df_out = combine_owner_sina_data()
    # print(df_out)
    run_download_owner_sina()

    # from scripts_stock.cfg.owner_url_list_sina import DataURLSina
    # data_url_sina = DataURLSina()
    # aa = [ data_url_sina.owner_abdb(),data_url_sina.owner_shebao()]
    # for owner_name, url in aa:
    #     print(owner_name)
    #     print(url)

    # owner_name, url = DataURLSina().owner_abdb()
    # # download_owner_sina(owner_name, url)
    # table, new_table_index = get_html_table(url)
    # df_out = parse_chigu_table_sina(table)
    # print(df_out)
