from scripts_stock.data_base.insert_into_db import insert_df_to_db, df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd
from scripts_stock.utils.logging_set import *


def fuquan_clean():
    return f"""
    select date,
    avg(open) as open,
    avg(close) as close,
    avg(high) as high,
    avg(low) as low,
    avg(transaction_volume) as transaction_volume,
    avg(transaction_cash) as transaction_cash
    from 
    r_t_hs300_etf  
    group by date
    """


conn = CommonScript.connect_to_db("prod.db")
df1 = pd.read_sql_query(fuquan_clean(), conn).round(2)

df_save_to_db(df1, "prod.db", "prd_clean_t_hs300_etf", if_there="replace")
conn.close()
