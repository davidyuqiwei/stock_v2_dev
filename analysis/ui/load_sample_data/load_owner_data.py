import json
import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess

import plotly.figure_factory as ff

from typing import Dict, List, Union

class OwnerSQl:
    def __init__(self):
        self.sql_str = ''
        self.base_table = 'r_t_owner_dfcf'
        self.return_df = ''
    def get_data_owner(self,owner_name):
        self.sql_str = f"""
        select SECUCODE,
        SECURITY_CODE as stock_index,
        SECURITY_NAME_ABBR as stock_name,
        HOLDER_NAME as owner_name,
        HOLD_NUM as hold_num,
        HOLDER_MARKET_CAP,
        FREE_HOLDNUM_RATIO as free_holdnum_ratio,
        HOLDER_STATEE,
        HOLDER_STATE_NEW,
        substr(UPDATE_DATE,1,10) as update_date,	
        REPORT_DATE_NAME,
        substr(END_DATE,1,10) as end_date,
        HOLDER_TYPE,
        HOLDNUM_CHANGE_NAME
        from 
        {self.base_table} where HOLDER_NAME='{owner_name}'
        and substr(END_DATE,1,10)='2024-09-30' limit 100
        """
        return self
    
    def get_holder_name(self):
        self.sql_str = f"""
            select distinct HOLDER_NAME,HOLDER_TYPE,
            substr(END_DATE,1,10) as update_date 
            from r_t_owner_dfcf 
            where HOLDER_TYPE<>'个人' and substr(END_DATE,1,10)='2024-09-30'
            limit 10
        """
        return self
    
    def get_holder_type(self):
        self.sql_str = f"""
            select HOLDER_TYPE,
            substr(END_DATE,1,10) as update_date 
            from r_t_owner_dfcf 
            where HOLDER_TYPE<>'个人' and substr(END_DATE,1,10)='2024-09-30'
        """
        return self
    
    def get_holder_name_from_type(self, input_holder_type):
        self.sql_str = f"""
            select distinct HOLDER_NAME,count(distinct SECURITY_CODE) as cnt
            from r_t_owner_dfcf 
            where HOLDER_TYPE='{input_holder_type}' and substr(END_DATE,1,10)='2024-09-30'
            group by HOLDER_NAME
        """
        return self
    
    def get_owner_holder_history(self, owner_name, stock_name):
        self.sql_str = f"""
        select distinct SECUCODE,
        SECURITY_CODE as stock_index,
        SECURITY_NAME_ABBR as stock_name,
        HOLDER_NAME as owner_name,
        HOLD_NUM as hold_num,
        HOLDER_MARKET_CAP,
        substr(END_DATE,1,10) as end_date
        from 
        {self.base_table} where HOLDER_NAME='{owner_name}' and SECURITY_NAME_ABBR='{stock_name}'
        limit 100
        """
        return self
    
    def main_run(self):
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(self.sql_str, conn)
        return df1.round(1)


def run_get_data_v1(input_str):
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(input_str, conn)
    return df1


owner_sql = OwnerSQl()
aa = owner_sql.get_holder_name_from_type("投资公司").main_run()
# print(aa["HOLDER_NAME"].to_list())

# owner_sql = OwnerSQl()
# owner_sql.get_data_owner("阿布达比投资局")
# aa = run_get_data_v1(owner_sql.sql_str)
# print(aa)
