import sqlite3
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.logging_set import TNLog
import pandas as pd

# conn = sqlite3.connect("test.db")
# cursor = conn.cursor()


def print_fuquan_all():
    import pandas as pd
    conn = CommonScript.connect_to_db("test.db")
    query = "SELECT * FROM prd_t_fuquan_dfcf order by date desc limit 20"
    
    # 使用pandas读取SQL查询结果
    df = pd.read_sql_query(query, conn)
    conn.close()
    # 打印出DataFrame的前几行
    print(df.head(10))


def print_all_table():
    conn = CommonScript.connect_to_db("test.db")
    cursor = conn.cursor()
    sql_query = "SELECT NAME FROM sqlite_master WHERE type='table'; "
    df = pd.read_sql_query(sql_query, conn)
    print(df.sort_values("name"))


# def check_table():
#     sql_query = """ owner_sina_t1"""
#     cursor.execute(sql_query)
#     print(cursor.fetchall())

def print_table_test(db,table_name="prd_t_owner_sina"):
    import pandas as pd
    conn = CommonScript.connect_to_db(db)
    TNLog().info("+++++++++ get sample data from DB +++++++")
    query = f"SELECT * FROM {table_name}  limit 1"
    # 使用pandas读取SQL查询结果
    df_test = pd.read_sql_query(query, conn)
    print(df_test)
    print("=============================")
    conn.close()
    # 打印出DataFrame的前几行

if __name__ == '__main__':
    #print("Aaaa")
    #print_table_test(db="test.db")
    print_all_table()



# cursor.execute("""CREATE TABLE books
#                   (title TEXT, author TEXT, release_date TEXT,
#                    publisher TEXT, book_type TEXT)
#                """)
    

"""
stock_name,hold_num,hold_ratio,stock_type,update_date
金宏气体,13534533,2.78,"流通A股,",2023-06-30
金宏气体,13140316,2.71,"流通A股,",2023-03-31
"""
# check_table()
#print_all_table()