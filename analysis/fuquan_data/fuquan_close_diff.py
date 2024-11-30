import math

from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
import os
from scripts_stock.utils.common import CommonScript
#from scripts_stock.utils.string_process import StringProcess
from scripts_stock.analysis.fuquan_data.get_data_sql import FGetDataSql # type: ignore
from scripts_stock.utils.datetime_process import get_years_before_date
from scripts_stock.analysis.fuquan_data.old.get_fuquan_index import StockIndex
from scripts_stock.data_base.insert_into_db import insert_df_to_db



def name_list():
    pre_str = "diff"
    get_str = []
    for i in [1,3,5,7]:
        get_str.append(pre_str + "_" + str(i) + "_ratio")
        get_str.append(pre_str + "_" + str(i)+"_cate")
    return get_str


def get_returns(df1) -> pd.DataFrame:
    import numpy as np
    diff1 = (df1['close'].shift(-1) - df1['close'])/df1['close']
    # diff1_cate = p_n_cate(diff1)
    df1['diff_1_ratio'] = diff1
    df1['diff_1_cate'] = np.where(df1['diff_1_ratio'] > 0, 1,np.where(df1['diff_1_ratio'] < 0,0, df1['diff_1_ratio']))

    df1['diff_3_ratio'] = (df1['close'].shift(-3) - df1['close'])/df1['close']
    df1['diff_3_cate'] = np.where(df1['diff_3_ratio'] > 0, 1,np.where(df1['diff_3_ratio'] < 0,0, df1['diff_3_ratio']))

    df1['diff_5_ratio'] = (df1['close'].shift(-5) - df1['close'])/df1['close']
    df1['diff_5_cate'] = np.where(df1['diff_5_ratio'] > 0, 1,np.where(df1['diff_5_ratio'] < 0,0, df1['diff_5_ratio']))

    df1['diff_7_ratio'] = (df1['close'].shift(-7) - df1['close'])/df1['close']
    df1['diff_7_cate'] =  np.where(df1['diff_7_ratio'] > 0, 1,np.where(df1['diff_7_ratio'] < 0,0, df1['diff_7_ratio']))
    df2 = df1.round(3)
    df3 = pd.DataFrame(df2[["date","stock_index","close"]+name_list()])
    return df3


def f_stock_return_fuquan(dir_stock_return_fuquan,date_cut):
    stock_diff_all = []
    stock_index_list = StockIndex(ProjectDir).get_fuquan_stock_index_all()
    for stock_index in stock_index_list:
        conn = CommonScript.connect_to_db("test.db")
        input_sql_str = FGetDataSql.get_data_sql_str_before_years(stock_index,date_cut)
        # print(input_sql_str)
        df1 = pd.read_sql_query(input_sql_str, conn)
        stock_diff_all.append(get_returns(df1))
        
    stock_diff_all_v1  = pd.concat(stock_diff_all)
    stock_diff_all_v1.to_csv(dir_stock_return_fuquan,index=0) # type: ignore

def aa(stock_index,date_cut):
    conn = CommonScript.connect_to_db("test.db")
    input_sql_str = FGetDataSql.get_data_sql_str_before_years(stock_index,date_cut)
    # print(input_sql_str)
    df1 = pd.read_sql_query(input_sql_str, conn)
    df1_re = get_returns(df1)
    return df1_re

if __name__ == '__main__':
    date_cut = get_years_before_date(10)
    dir_stock_return_fuquan = os.path.join(ProjectDir.analysis_data_dir,"stock_return_fuquan.csv")
    f_stock_return_fuquan(dir_stock_return_fuquan,date_cut)
    insert_df_to_db(dir_stock_return_fuquan,"t_stock_return_fuquan")
    '''
    date_cut = get_years_before_date()
    a1 = aa("601398",date_cut)
    print(a1.tail(10))
   
    '''

# print(stock_diff_all_v1.head(10))



# #print(name_list())
# # df2 = get_returns(df1)
# print(stock_diff_all_v1.tail(20))