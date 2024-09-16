# coding: utf-8
import stockstats
import pandas as pd


# import matplotlib.pyplot as plt
# from davidyu_cfg import *
# from functions.LinearReg import *


def date_trans(x):
    x1 = int(x.replace("-", ""))
    return x1


def df_to_stock_df(df1):
    df1 = df1.sort_values('stock_date').drop_duplicates()
    df1.rename(columns={'stock_date': 'date'}, inplace=True)
    #print(df1)
    df1.date = df1.date.apply(date_trans)
    # print(df1.head())
    stock = stockstats.StockDataFrame.retype(df1)
    # print(stock.head())
    stock['date_time'] = pd.to_datetime(stock.index, format='%Y%m%d')
    stock.index = pd.to_datetime(stock.index, format='%Y%m%d')
    return stock


def select_data(stock, start_date, end_date):
    date_select = (stock.date_time > start_date) & (stock.date_time < end_date)
    stock1 = stock[date_select]
    return stock1


def stock_kdj(stock, feature_list=None):
    if feature_list is None:
        feature_list = ["macdh", "cci", "rsi_6", "rsi_12", "rsi_24", "kdjk", "kdjd", "kdjj", "boll_ub", "boll_lb",
                        "macd", "macds",
                        "wr_6", "wr_10"]
    # df_kdj = stock[['kdjk','kdjd','kdjj']].reset_index()
    df_kdj = stock.reset_index()
    df_kdj['stock_index'] = stock['stock_index'].tolist()
    df_kdj['stock_date'] = df_kdj['date']
    df_kdj['stock_date'] = df_kdj['stock_date'].astype(str)
    for k in feature_list:
        df_kdj[k] = stock[k].reset_index()[k]
    return df_kdj, feature_list


def stock_feature(stock, feature_list):
    df_kdj = stock[feature_list].reset_index()
    df_kdj['stock_index'] = stock['stock_index'].tolist()
    df_kdj['stock_date'] = df_kdj['date'].astype(str)
    return df_kdj


def add_new_feature(df_stock):
    df_raw_col = df_stock.columns.tolist()
    stock = df_to_stock_df(df_stock)
    new_col_list = []
    for i in range(5,20):
        stockstats.StockDataFrame.KDJ_WINDOW=i
        stock1 = df_to_stock_df(df_stock)
        new_col1 = "kdjk_"+str(i)
        new_col2 = "kdjd_"+str(i)
        new_col3 = "kdjj_"+str(i)
        stock[new_col1] = stock1["kdjk"]
        stock[new_col2] = stock1["kdjd"]
        stock[new_col3] = stock1["kdjj"]
        add_list = [new_col1,new_col2,new_col3]
        new_col_list = new_col_list + add_list
    new_rsi = []
    new_wr = []
    for i in range(5,30):
        new_rsi.append("rsi_"+str(i))
        new_wr.append("wr_"+str(i))
    feature_list = ['kdjk','kdjd','kdjj','macdh','cci']
    all_feature = new_rsi+new_wr+feature_list+new_col_list
    all_feature = list(set(all_feature))
    df_out = stock[all_feature].reset_index()
    return df_out,all_feature
