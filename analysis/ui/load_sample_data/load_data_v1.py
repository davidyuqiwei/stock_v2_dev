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

def get_daily_data():
    return """select t1.*,t2.stock_name from t_stock_kdj_daily_last t1
left join prd_t_hs300 t2
on t1.stock_index=t2.stock_index"""


def get_data_owner(owner_name):
    return f"""select * from m_owner_stock_name_price_hs300 where owner_name='{owner_name}'"""

def get_data_owner_list():
    return f"""select distinct owner_name,update_date from m_owner_stock_name_price_hs300 """


def get_weekly_kdj_data():
    return """
    select t1.*,t2.stock_name from t_stock_kdj_weekly_last t1
    left join prd_t_hs300 t2
    on t1.stock_index=t2.stock_index
    """


def get_weekly_kdj_data_last5():
    return """
    select t1.*,t2.stock_name from t_stock_kdj_weekly_last5 t1
    left join prd_t_hs300 t2
    on t1.stock_index=t2.stock_index
    """

def get_sample_data():
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(get_daily_data(), conn)
    df1["stock_index"] =df1["stock_index"].astype(str)
    df2 = pd.read_sql_query(get_weekly_kdj_data(), conn)
    df2["stock_index"] = df2["stock_index"].astype(str)

    df3 = pd.read_sql_query(get_weekly_kdj_data_last5(), conn)
    df3["stock_index"] = df3["stock_index"].astype(str)
    return df1,df2,df3


def get_sample_data_owner(owner_name):
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(get_data_owner(owner_name),conn)
    return df1


def run_get_data_owner_list():
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(get_data_owner_list(),conn)
    return df1


def format_dates(date_list) -> Dict:
    formatted_dates = {}
    df1 = run_get_data_owner_list()
    #dates = df1["update_date"].unique().tolist()
    for date in date_list:
        # print(date)
        year, month, date_in = date.split('-')
        if year not in formatted_dates:
            formatted_dates[year] = {}
        #print(f"{year}-{month}-{date_in}")
        formatted_dates[year][f"{year}-{month}-{date_in}"] = f"{year}-{month}-{date_in}"

        # 打印结果
    import json
    #print(json.dumps(formatted_dates, indent=4, ensure_ascii=False))
    out = json.dumps(formatted_dates, indent=4, ensure_ascii=False)

    return json.loads(out)



if __name__ == '__main__':
    df1 = run_get_data_owner_list()
    #print(df1["update_date"].unique().tolist()+["full"])
    aa = format_dates( df1["update_date"].unique().tolist())
    print(type(aa))
