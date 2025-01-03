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

today_date, _, one_month_ago = date_today_yesterday(30)
def get_sample_cash_flow(stock_index_in=601398):
    sql_str = f"""
    select  stock_index,date,
	 small_order_net_inflow_amount,medium_order_net_inflow_amount,
     large_order_net_inflow_amount,
     super_large_order_net_inflow_amount
     from r_t_cash_flow_stocks 
     where stock_index={stock_index_in}
    ;
    """
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(sql_str, conn)
    return df1


def get_sample_cash_flow_ratio(stock_index_in=601398):
    sql_str = f"""
    select  stock_index,date,
	   super_large_order_net_inflow_amount_ratio
     from cal_t_stocks_cash_flow_ratio 
     where stock_index={stock_index_in}
    ;
    """
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(sql_str, conn)
    return df1


def get_ample_cash_flow_ratio_recent(today_date=today_date, one_month_ago=one_month_ago):
    sql_str = f"""
    select t1.stock_index,t2.stock_name,
    date,super_large_order_net_inflow_amount_from_df1 as super_large_amount,
    super_large_order_net_inflow_amount_ratio as super_large_amount_ratio,
    large_order_net_inflow_amount_from_df1 as large_amount,
    large_order_net_inflow_amount_ratio as large_amount_ratio
    from (
        select * from cal_t_stocks_cash_flow_ratio
        where (large_order_net_inflow_amount_ratio=1 
        or super_large_order_net_inflow_amount_ratio=1)
        and date>='{one_month_ago}' and date<='{today_date}'
    ) t1
    inner join 
    prd_t_all_stock_index_name t2
    on t1.stock_index=t2.stock_index
    """
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(sql_str, conn)
    print(sql_str)
    return df1
