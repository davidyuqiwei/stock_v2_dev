import sqlite3
from scripts_stock.utils.common import CommonScript

conn = sqlite3.connect("test.db")
cursor = conn.cursor()


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
    sql_query = """SELECT name FROM sqlite_master
        WHERE type='table';"""
    cursor.execute(sql_query)
    print(cursor.fetchall())


def check_table():
    sql_query = """ owner_sina_t1"""
    cursor.execute(sql_query)
    print(cursor.fetchall())


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
print_fuquan_all()
#print_all_table()