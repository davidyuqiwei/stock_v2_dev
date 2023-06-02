# -*- coding: utf-8 -*-            
# @Time : 2023/6/2 22:18
# @Author: Davidyu
# @FileName: url_list.py
class DataURL:
    def __init__(self):
        self.test = ""

    def owner_shebao_url(self):
        return "owner_shebao","https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123044164703831989427_1685715273131&reportName=RPT_COOPFREEHOLDERS_ANALYSIS&columns=HOLDER_NAME%2CCOOPERATION_HOLDER_MARK&source=WEB&client=WEB&distinct=HOLDER_NAME&filter=(HOLDER_NAME+like+%22%25%E7%A4%BE%E4%BF%9D%25%22)(END_DATE%3E%3D%272018-06-02%27)&_=1685715273132"

    def owner_hk_url(self):
        return "owner_hk","https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123038334412448220223_1685711284341&sortColumns=END_DATE%2CHOLDNUM_CHANGE_TYPE&sortTypes=-1%2C1&pageSize=50&pageNumber=1&columns=ALL&source=WEB&client=WEB&filter=(COOPERATION_HOLDER_MARK%3D%2210671586%22)(END_DATE%3E%3D%272015-03-31%27)&reportName=RPT_COOPFREEHOLDERS_ANALYSIS"