from scripts_stock.data_base.insert_into_db import insert_df_to_db,df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd


def owner_mid_table():
    return """
    select t1.*,t_name.stock_index,t2.date as stock_price_date,t2.close as close
    FROM
    prd_t_owner_sina t1
    left join prd_t_all_stock_index_name t_name
    on trim(t1.stock_name)=trim(t_name.stock_name)
    left join 
    prd_t_fuquan_dfcf t2
    on  t_name.stock_index=t2.stock_index and 
        (julianday(t1.update_date)-julianday(t2.date))<=30 and 
        (julianday(t1.update_date)-julianday(t2.date))>=0
    """
conn = CommonScript.connect_to_db("test.db")
cursor = conn.cursor()
df1 = pd.read_sql_query(owner_mid_table(),conn)
table_name = "m_owner_stock_name_price"
df_save_to_db(df1,target_table=table_name)

def owner_mid_table_hs300(input_table):
    return f"""
    select stock_name,stock_index,owner_name,hold_num,update_date,round(avg(close),2) as avg_close,
    round(avg(close)*avg(hold_num),0) as cash_hold
    from
    (
        select * from {input_table}
        where close is not null
    ) 
    group by stock_name,stock_index,owner_name,hold_num,update_date
    """
conn = CommonScript.connect_to_db("test.db")
cursor = conn.cursor()
input_table = "m_owner_stock_name_price"
out_table_name = "m_owner_stock_name_price_hs300"
df1 = pd.read_sql_query(owner_mid_table_hs300(input_table),conn)
df_save_to_db(df1,target_table=out_table_name)


#insert_df_to_db