from scripts_stock.data_base.insert_into_db import insert_df_to_db,df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd
from scripts_stock.utils.logging_set import *

etl_table_list = [
    "prd_t_owner_sina",
    "prd_t_fuquan_dfcf",
    "prd_t_hs300_daily"
]

def etl_test_to_prod(input_table):
    return f"""
    select * from {input_table}
    """

for table_in in etl_table_list:
    conn = CommonScript.connect_to_db("test.db")
    df1 = pd.read_sql_query(etl_test_to_prod(table_in),conn)
    conn.close()

    conn = CommonScript.connect_to_db("prod.db")
    df_save_to_db(df1,"prod.db",table_in)
    conn.close()
    TNLog().info("==== +++++  finish all table from test to PROD ++++++ =====")