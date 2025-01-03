import json
import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
from scripts_stock.utils.datetime.date_function import date_today_yesterday


class DataCheck():

    def __init__(self):
        # self.stock_list = GetDataFromDB.db_get_hs300_list(if_str=True)
        self.save_tmp_txt_dir = ''
        self.tmp_data_txt_name = ''
        # self.save_csv_dir = ProjectDir.parse_data_dir_bankuai_cash_flow
        self.final_data_name = ""

        self.table_list = ['prd_t_fuquan_dfcf',
                           'r_t_cash_flow_stocks']
        self.table_list_v2 = ['r_t_hs300_etf']
        self.table = ''
        self.all_table = self.table_list+self.table_list_v2

    def basic_data_inform(self):
        sql_str = f"""
        select '{self.table}' as table_name,
        min(date) as min_data_date,
        max(date) as max_data_date,
        count(distinct stock_index) as stock_index_cnt,
        count(1) as total_rows_cnt,
        max(update_time) as update_time

        from {self.table} 
        
        """
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(sql_str, conn)
        return df1

    def basic_data_inform_v2(self):
        sql_str = f"""
        select '{self.table}' as table_name,
        min(date) as min_data_date,
        max(date) as max_data_date,
        count(1) as total_rows_cnt,
        max(update_time) as update_time

        from {self.table} 
        
        """
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(sql_str, conn)
        return df1

    def check_basic_infor(self):
        df_list = []

        for table_in in self.table_list:
            self.table = table_in
            df1 = self.basic_data_inform()
            df_list.append(df1)
        df_out = pd.concat(df_list)
        return df_out

    def check_basic_infor_v2(self):
        df_list = []

        for table_in in self.table_list_v2:
            self.table = table_in
            df1 = self.basic_data_inform_v2()
            df_list.append(df1)
        df_out = pd.concat(df_list)
        return df_out

    @staticmethod
    def sample_data(table_name='r_t_fin_report'):
        sql_str = f"""
        select * from {table_name} 
        order by random()
        limit 100
        """
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(sql_str, conn)
        return df1

    def main_run(self):
        df2 = self.check_basic_infor()
        df3 = self.check_basic_infor_v2()
        return df2, df3


if __name__ == "__main__":
    a1, a2 = DataCheck().main_run()
    print(a1)
    print(a2)
