# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:20
# @Author: Davidyu
# @FileName: owner_data_dfcf.py

import wget  # 导入wget库
import os
from script_stock.cfg.url_list.owner_url_list_dfcf import DataURL


def run_download_owner_data(save_data_dir):
    owner_name, url = DataURL().owner_shebao_url()
    save_name = os.path.join(save_data_dir, owner_name + ".txt")
    wget.download(url, save_name)

    owner_name, url = DataURL().owner_hk_url()
    save_name = os.path.join(save_data_dir, owner_name + ".txt")
    wget.download(url, save_name)


if __name__ == '__main__':
    run_download_owner_data()

