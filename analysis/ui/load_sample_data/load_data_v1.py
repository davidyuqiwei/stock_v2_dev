import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess

import plotly.figure_factory as ff


def get_data():
    return """select t1.*,t2.stock_name from t_stock_kdj_daily_last t1
left join prd_t_hs300 t2
on t1.stock_index=t2.stock_index"""

def get_sample_data():
    conn = CommonScript.connect_to_db("test.db")
    cursor = conn.cursor()
    df1 = pd.read_sql_query(get_data(),conn)
    df1["stock_index"] =df1["stock_index"].astype(str)
    return df1


if __name__ == '__main__':
    df1 = get_sample_data()
    print(df1.columns)

