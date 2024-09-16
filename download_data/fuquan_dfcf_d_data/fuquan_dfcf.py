# -*- coding: utf-8 -*-            
# @Time : 2023/8/22 15:33
# @Author: Davidyu
# @FileName: fuquan_dfcf.py

#from telnetlib import PRAGMA_HEARTBEAT
import wget  # 导入wget库
from scripts_stock.cfg.set_dir import *


# https://quote.eastmoney.com/sh601138.html#

def download_fuquan_data(stock_index, save_data_dir):
    input_stock_index = ""
    if stock_index[0:2] =="60" or stock_index[0:2] == "00":
        if stock_index[0:2] == "60":
            input_stock_index = "1." + stock_index
        if stock_index[0:2] == "00":
            input_stock_index = "0." + stock_index

        url1 = f"http://93.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112409381248828282374_1609254428957&secid={input_stock_index}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt=3000&_=1609254428987"

        # print(url1)
        data_name = "fuquan_" + stock_index
        save_name = os.path.join(save_data_dir, data_name + ".txt")
        wget.download(url1, save_name)
        return save_name


if __name__ == '__main__':
    stock_index = "601398"
    project_dir = ProjectDir()
    download_fuquan_data(stock_index, project_dir.download_data_dir_fuquan)
