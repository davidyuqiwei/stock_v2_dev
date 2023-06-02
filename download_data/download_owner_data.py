# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:20
# @Author: Davidyu
# @FileName: download_owner_data.py
import wget  # 导入wget库
import os
from scripts_stock.download_data.url_list import DataURL


def run_download_data(download_data_dir):
    owner_name, url = DataURL().owner_shebao_url()
    save_name = os.path.join(download_data_dir, owner_name + ".txt")
    wget.download(url, save_name)

    owner_name, url = DataURL().owner_hk_url()
    save_name = os.path.join(download_data_dir, owner_name + ".txt")
    wget.download(url, save_name)

if __name__ == '__main__':
    run_download_data()