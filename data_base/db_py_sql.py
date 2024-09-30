

def get_fuquan_stock_index_sql_str():
    return """
                SELECT distinct stock_index 
                FROM prd_t_fuquan_dfcf  
            """

def get_all_fuquan_one_stock(stock_index):
    return f"""SELECT *  FROM prd_t_fuquan_dfcf  where stock_index= {stock_index}"""

def get_sina_onwer_all():
    return  "select * from prd_t_owner_sina"

def all_stock_index():
    return  "select distinct_stock_index from prd_t_all_stock_index_name"