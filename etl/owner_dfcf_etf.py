import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
from scripts_stock.data_base.insert_into_db import insert_df_to_db, df_save_to_db


def get_data_sql_str():
    return f"""SELECT * from r_t_owner_dfcf
        where substr(END_DATE,1,4)>='2018'
    """


conn = CommonScript.connect_to_db("test.db")
cursor = conn.cursor()
df1 = pd.read_sql_query(get_data_sql_str(), conn)

df_save_to_db(df1, target_table="r_t_owner_dfcf_2018_onwards", if_there="replace")
