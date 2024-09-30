import sqlite3
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.logging_set import TNLog
import pandas as pd
from scripts_stock.data_base.cfg import DBTableName
from scripts_stock.data_base.db_py_sql import *



class GetDataFromDB:
     
    @staticmethod
    def db_get_hs300_list(if_str=False):
        conn = CommonScript.connect_to_db("test.db")
        cursor = conn.cursor()
        sql_query = f"SELECT stock_index FROM {DBTableName.table_sh300_name()} "
        df = pd.read_sql_query(sql_query, conn)
        raw_list = df["stock_index"].tolist()
        if if_str:
            return [ str(x).zfill(6) for x in raw_list]
        else:
            return  raw_list
        
    @staticmethod
    def get_fuquan_stock_index_all():
        conn = CommonScript.connect_to_db("test.db")
        cursor = conn.cursor()
        #sql_query_stock_index = 
        stock_list_in = cursor.execute(get_fuquan_stock_index_sql_str()).fetchall()
        stock_index_list = [x[0] for x in stock_list_in]
        conn.close()
        return stock_index_list

    @staticmethod
    def get_fuquan_all_one_stock_df(stock_index):
        conn = CommonScript.connect_to_db("test.db")
        cursor = conn.cursor()
        #sql_query_stock_index = 
        input_sql_str = get_all_fuquan_one_stock(stock_index)
        df1 = pd.read_sql_query(input_sql_str, conn)
        conn.close()
        return df1
    
    @staticmethod
    def get_sina_onwer_all_df():
        conn = CommonScript.connect_to_db("test.db")
        df1 = pd.read_sql_query(get_sina_onwer_all(), conn)
        conn.close()
        return df1
    
    @staticmethod
    def get_all_stock_index(if_str=False):
        conn = CommonScript.connect_to_db("test.db")
        cursor = conn.cursor()
        
        sql_query = f"SELECT stock_index FROM prd_t_all_stock_index_name"
        df = pd.read_sql_query(sql_query, conn)
        raw_list = df["stock_index"].tolist()
        if if_str:
            return [ str(x).zfill(6) for x in raw_list]
        else:
            return  raw_list
        
    @staticmethod
    def get_stock_indicator(if_str=False,target_db="test.db"):
        conn = CommonScript.connect_to_db(target_db)
        
        sql_query = f"SELECT * FROM t_stock_kdj_weekly_last60"
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df







if __name__ == "__main__":
    #a1 = getDataFromDB.db_get_hs300_list()
    a1 = GetDataFromDB.get_fuquan_stock_index_all()
    print(a1)