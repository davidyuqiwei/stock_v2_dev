
import stat


class DBTableName:
    @staticmethod
    def table_sh300_name():
        return "prd_t_hs300"
    @staticmethod
    def table_all_stock_index_name():
        return "prd_t_all_stock_index_name"
    
    @staticmethod
    def table_all_stock_close_sep():
        return "prd_t_all_stock_close_sep"

    @staticmethod
    def table_hs300_etf():
        return "r_t_hs300_etf"

    @staticmethod
    def table_owner_dfcf():
        return "r_t_owner_dfcf"

    @staticmethod
    def table_fin_report():
        return "r_t_fin_report"
    
    @staticmethod
    def cash_flow_stocks():
        return "r_t_cash_flow_stocks"
