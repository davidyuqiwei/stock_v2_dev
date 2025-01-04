from scripts_stock.data_base.insert_into_db import insert_df_to_db, df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd
from scripts_stock.utils.logging_set import *

def fuquan_clean():
    return f"""
    select date,stock_index,
    avg(open) as open,
    avg(close) as close,
    avg(high) as high,
    avg(low) as low,
    avg(transaction_volume) as transaction_volume
    from 
    prd_raw_t_fuquan_dfcf  
    group by date,stock_index
    """

conn = CommonScript.connect_to_db("prod.db")
df1 = pd.read_sql_query(fuquan_clean(), conn).round(2)

df_save_to_db(df1, "prod.db", "prd_clean_t_fuquan_dfcf",if_there="replace")
conn.close()
