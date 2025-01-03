from scripts_stock.data_base.insert_into_db import insert_df_to_db,df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd
from scripts_stock.utils.logging_set import *


def get_all_table_list(db="prod.db"):    
    conn = CommonScript.connect_to_db(db)

    # 创建一个游标对象
    cursor = conn.cursor()

    # 查询 sqlite_master 表，获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # 获取所有结果
    tables = cursor.fetchall()
    table_list = []
    for table in tables:
        table_list.append(table[0])
    conn.close()
    return table_list

def create_temp_table(input_table):
    return f"""
    select * from {input_table}
    """
def deduplicates_all_tables(table_list,db="prod.db"):
    conn = CommonScript.connect_to_db(db)
    for table_in in table_list:
        try:
            df1 = pd.read_sql_query(create_temp_table(table_in),conn)
            df2 = df1.drop(columns=['update_time']).drop_duplicates()
            df_save_to_db(df2, db, table_in, "replace")
        except Exception as e:
            TNLog().error("=== ETL test to PROD error =====")
            TNLog().error(e)
            TNLog().error(table_in)
            pass
    conn.close()
    TNLog().info("==== +++++  finish all table drop duplicates in PROD ++++++ =====")


def deduplicates_one_tables(table_in="r_t_owner_dfcf", db="test.db"):
    conn = CommonScript.connect_to_db(db)

    try:
        df1 = pd.read_sql_query(create_temp_table(table_in), conn)
        df2 = df1.drop(columns=['update_time']).drop_duplicates()
        df_save_to_db(df2, db, table_in, "replace")
        TNLog().info(
            f"==== +++++  finish  table {table_in} drop duplicates in {db} ++++++ =====")
    except Exception as e:
        TNLog().error("=== drop table duplicates error =====")
        TNLog().error(e)
        TNLog().error(table_in)
        pass


if __name__ == "__main__":
    tables = get_all_table_list("prod.db")
    print(tables)
    deduplicates_all_tables(tables, "prod.db")
    
    tables = get_all_table_list("test.db")
    print(tables)
    deduplicates_all_tables(tables,"test.db")
    

    # conn = CommonScript.connect_to_db("test.db")
    deduplicates_one_tables()
