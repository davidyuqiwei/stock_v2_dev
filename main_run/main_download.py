# -*- coding: utf-8 -*-
# @Time : 2023/8/29 22:45
# @Author: Davidyu
# @FileName: main_download.py

from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import StockList
from scripts_stock.download_data.owner_sina.owner_data_sina import run_download_owner_sina
from scripts_stock.utils.logging_set import *
from scripts_stock.data_base.insert_into_db import fuquan_data_insert_to_db

from scripts_stock.download_data.fuquan_dfcf_d_data.download_fuquan_dfcf_data import (
    download_fuquan_schedule,
    run_download_fuquan_schedule,
)


if __name__ == "__main__":
    run_download_fuquan_schedule("test")
    fuquan_data_insert_to_db()
    run_download_owner_sina()
    TNLog().info("===*** Finish download data and save to DB ***====")

