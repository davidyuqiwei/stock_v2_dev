# -*- coding: utf-8 -*-            
# @Time : 2023/8/29 23:06
# @Author: Davidyu
# @FileName: string_process.py
class StringProcess:
    @staticmethod
    def parse_latin(x):
        try:
            gbk_str = x.encode("latin1").decode("gbk").strip()
            return gbk_str
        except:
            return x
        
    @staticmethod
    def int_to_stock_index(x):
        try:
            x1 = str(int(x))[0:6].zfill(6)
            return x1
        except:
            return "no"