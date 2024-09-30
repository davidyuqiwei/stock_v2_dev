

class FGetDataSql():
    @staticmethod
    def get_data_sql_str(stock_index):
        return f"""SELECT *  FROM prd_t_fuquan_dfcf  where stock_index= {stock_index}"""
    
    @staticmethod
    def get_data_sql_str_before_years(stock_index,date_after):
        return f"""SELECT *  FROM prd_t_fuquan_dfcf  where stock_index= {stock_index} and date>='{date_after}'"""
    

    @staticmethod
    def get_distinct_stock_index_infuquan():
        return f"""SELECT distinct stock_index FROM prd_t_fuquan_dfcf """