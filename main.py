# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:27
# @Author: Davidyu
# @FileName: main.py

from scripts_stock.download_data.download_owner_data import *
from scripts_stock.cfg.set_dir import download_data_dir, current_dir, project_dir


run_download_data(download_data_dir)