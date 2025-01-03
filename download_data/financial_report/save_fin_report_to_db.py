import os
import pandas as pd
from scripts_stock.data_base.insert_into_db import insert_df_to_db
from scripts_stock.download_data.financial_report.download_fin_report_history import *
from scripts_stock.cfg.set_dir import ProjectDir



hs300_cfg = DownloadFinReport(ProjectDir)
filename = hs300_cfg.final_data_name
df1 = pd.read_csv(filename)
print(df1.columns)
insert_df_to_db(filename, "r_t_fin_report")
TNLog().info("==== +++++  save financial report data into DB ++++++ =====")

raw_col = ['SECURITY_CODE', 'SECURITY_NAME_ABBR', 'TRADE_MARKET_CODE',
           'TRADE_MARKET', 'SECURITY_TYPE_CODE', 'SECURITY_TYPE', 'UPDATE_DATE',
           'REPORTDATE', 'BASIC_EPS', 'DEDUCT_BASIC_EPS', 'TOTAL_OPERATE_INCOME',
           'PARENT_NETPROFIT', 'WEIGHTAVG_ROE', 'YSTZ', 'SJLTZ', 'BPS', 'MGJYXJJE',
           'XSMLL', 'YSHZ', 'SJLHZ', 'ASSIGNDSCRPT', 'PAYYEAR', 'PUBLISHNAME',
           'ZXGXL', 'NOTICE_DATE', 'ORG_CODE', 'TRADE_MARKET_ZJG', 'ISNEW',
           'QDATE', 'DATATYPE', 'DATAYEAR', 'DATEMMDD', 'EITIME', 'SECUCODE']


col_name = [
    "stock_index",
    "stock_name",
    "TRADE_MARKET_CODE",
    "TRADE_MARKET",
    "SECURITY_TYPE_CODE",
    "SECURITY_TYPE",
    "UPDATE_DATE",
    "REPORTDATE",
    "每股收益",
    "DEDUCT_BASIC_EPS",
    "营业总收入",
    "净利润",
    "净资产收益率",
    "营业总收入同比增长率",
    "净利润同比增长率",
    "每股净资产",
    "每股经营现金流",
    "销售毛利率",
    "营业总收入季度环比增长",
    "净利润季度环比增长",
    "分红",
    "PAYYEAR",
    "行业",
    "ZXGXL",
    "NOTICE_DATE",
    "ORG_CODE",
    "TRADE_MARKET_ZJG",
    "ISNEW",
    "QDATE",
    "DATATYPE",
    "DATAYEAR",
    "DATEMMDD",
    "EITIME",
    "SECUCODE"
]
