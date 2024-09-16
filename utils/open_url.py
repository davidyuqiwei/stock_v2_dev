# -*- coding: utf-8 -*-            
# @Time : 2023/8/21 10:32
# @Author: Davidyu
# @FileName: open_url.py
import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as BS


def url_opener(url):
    # opener = urllib2.dbuild_opener()
    # opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    values = {'act': 'login'}
    # req = urllib.request.Request(url, values, headers)
    response = urllib.request.urlopen(url)
    # response = urllib2.urlopen(u1)
    soup_u1 = BS(response, "html.parser")
    return soup_u1


def get_html_table(url1):
    soup2 = url_opener(url1)
    table = soup2.find_all('tbody')[1]
    new_table_index = [x for x in range(0, len(table.find_all('tr')))]
    return table, new_table_index


"""
def table_to_DF(table, new_table_index, DF_columns):
    new_table = pd.DataFrame(columns=range(0, DF_columns), index=new_table_index)
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('th') + row.find_all('td')
        for column in columns:
            try:
                new_table.iat[row_marker, column_marker] = column.get_text().encode("latin1").decode("gbk").strip()
            except:
                new_table.iat[row_marker, column_marker] = column.get_text().strip()
            column_marker += 1
        row_marker += 1
    new_table = new_table.dropna(axis=0)
    return new_table

"""

if __name__ == '__main__':
    url1 = "https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=000887&stockholderid=70010102"
    url1 = "https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=000887&stockholderid=80128964"
    table, new_table_index = get_html_table(url1)
    # print(a1)
    # new_table = table_to_DF(table, new_table_index, 8)

    #
    # a3 = a2.get_text()
    # a4 = a3.split(" ")

    print(new_table)
