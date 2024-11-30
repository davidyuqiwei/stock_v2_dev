import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
from scripts_stock.data_base.insert_into_db import insert_df_to_db,df_save_to_db
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.data_base.db_py_sql import get_all_fuquan_one_stock
from scripts_stock.utils.logging_set import *
from scripts_stock.analysis.fuquan_data.local_peak_find.find_peaks import *


df_weekly_peak = []

class LocalPeak():
    def __init__(self):
        self.stock_list = GetDataFromDB.get_fuquan_stock_index_all()
        
    #stock_index = "601658"
    def loop_get_peak(self):
        for ind in self.stock_list[0:3]:

            df1 = GetDataFromDB.get_fuquan_all_one_stock_df(ind)
            df2 = df1[df1["date"]>='2018-01-01']
            df_weekly= df2.groupby(lambda x:math.floor(x/5)).last()
            delta_in = np.mean(df_weekly['close'])/10
            series = df_weekly['close']
            minpeaks, maxpeaks = findpeaks(series, DELTA=delta_in)

            max_index = [x[0] for x in maxpeaks]
            min_index = [x[0] for x in minpeaks]

            df_weekly["local_peak"] = 0
            df_weekly.loc[max_index,"local_peak"]=1
            df_weekly.loc[min_index,"local_peak"]=-1
            df_weekly1 = df_weekly.reset_index(drop=True)
            df_weekly_peak.append(df_weekly1.drop(0)[["date","close","stock_index","local_peak"]])

        df_out1 = pd.concat(df_weekly_peak,sort=False)

        return df_out1


if __name__ == "__main__":
    local_peak = LocalPeak()
    aa = local_peak.loop_get_peak()
    print(aa)