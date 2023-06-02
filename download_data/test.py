# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:15
# @Author: Davidyu
# @FileName: test.py
import wget  #导入wget库

url="https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123044164703831989427_1685715273131&reportName=RPT_COOPFREEHOLDERS_ANALYSIS&columns=HOLDER_NAME%2CCOOPERATION_HOLDER_MARK&source=WEB&client=WEB&distinct=HOLDER_NAME&filter=(HOLDER_NAME+like+%22%25%E7%A4%BE%E4%BF%9D%25%22)(END_DATE%3E%3D%272018-06-02%27)&_=1685715273132"
do = wget.download(url,"test.txt")
print(do)


