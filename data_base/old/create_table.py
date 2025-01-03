import sqlite3
from scripts_stock.cfg.set_dir import *
from scripts_stock.data_base.old.create_table_structure import create_table, get_df_column_type_sqllite, make_column_str
import pandas as pd


def get_create_table_str(target_db = "test.db",table_name="owner_sina",col_str=""):
    #target_db = "test.db"

    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()
    # create a table
    cursor.execute(f"""CREATE TABLE {table_name}
                    ({col_str})
                """)
    
    conn.commit()
    print(f"============== create table {table_name} =================")
    print(f"============== create table {col_str} =================")
    return conn



def create_table(database,table_name,input_df):
    col_type = get_df_column_type_sqllite(input_df)
    comment = input_df.columns
    #print(col_type)
    column_str = make_column_str(input_df.columns,col_type,comment)
    #print(column_str)
    conn = get_create_table_str(database,table_name,column_str)
    return conn


if __name__=='__main__':
    #test()
    database = os.path.join(ProjectDir.database_dir,"test.db")
    table_name = "prd_t_fuquan_dfcf"
    #df1 = pd.read_csv(os.path.join(ProjectDir.download_sample_data_dir,"sina_owner_abudabi.csv"),encoding="utf-8-sig")
    df1 = pd.read_csv(os.path.join(ProjectDir.download_data_dir_fuquan,"fq_000001.csv"),encoding="utf-8-sig")

    conn = create_table(database,table_name,df1)

    #df1.to_sql(table_name,conn,if_exists='replace',index=False)
