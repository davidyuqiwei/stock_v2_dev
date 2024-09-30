import math
from scripts_stock.cfg.out_file_name import OutFileName
from scripts_stock.cfg.set_dir import ProjectDir
from scripts_stock.cfg.stock_list import *
from scripts_stock.utils.analysis.stock_stat_index import df_to_stock_df, stock_kdj
import os
from scripts_stock.utils.common import CommonScript
from scripts_stock.utils.string_process import StringProcess
import numpy as np
import lightgbm as lgb


def get_data_sql_str(table):
    return f"""SELECT *  FROM {table} limit 10 """

def get_data_sql_str_macd(stock_index):
    return f"""SELECT *  FROM t_stock_kdj_daily_all where date>='2022-9-23' and stock_index={stock_index} """

def get_train_data():
    aa = f"""
    select t1.*,t2.diff_5,t2.diff_3_cate,t2.diff_5_cate,t2.diff_7_cate
    from t_stock_kdj_daily_all AS t1
    join t_stock_return_fuquan AS t2
    on t1.date=t2.date and t1.stock_index=t2.stock_index
    where close<8 and t2.date<='2024-09-01' and t2.date>="2022-01-01"
    """
    return aa

def get_predict_data():
    aa = f"""
    select t1.*,t2.diff_5,t2.diff_3_cate,t2.diff_5_cate,t2.diff_7_cate
    from t_stock_kdj_daily_all AS t1
    join t_stock_return_fuquan AS t2
    on t1.date=t2.date and t1.stock_index=t2.stock_index
    where close<8 and t2.date>='2024-09-01'
    """
    return aa

def get_train_df(df_pred_y):
    conn = CommonScript.connect_to_db("test.db")
    cursor = conn.cursor()
    df1 = pd.read_sql_query(get_train_data(),conn)
    # df1 = df1[df1["stock_index"]==601398]
    df1["boll_diff"]= df1["boll_ub"] - df1["boll_lb"]
    #df1.columns
    features = [ 'macdh', 'cci', 'rsi_6', 'rsi_12', 'rsi_24', 'kdjk',
        'kdjd', 'kdjj', 'boll_ub', 'boll_lb','boll_diff', 'macd', 'macds', 'wr_6', 'wr_10']
    #df_pred_y = ['diff_3_cate']

    df2 = df1[features+df_pred_y].dropna()
    print(df2.shape)
    return df2,features,df_pred_y

def f_importance(bst):
    feature_importance  = pd.DataFrame()
    feature_importance['fea_name'] = features
    feature_importance['fea_imp']  = bst.feature_importances_
    feature_importance = feature_importance.sort_values('fea_imp',ascending = False)


def r_train_model(df2,features,df_pred_y):
    from sklearn import tree#导入模块
    from sklearn.model_selection import train_test_split
  

    X = df2[features]
    Y = df2[df_pred_y[0]]
    print("======= training data shape ======")
    print(X.shape)
    x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2)
    print(y_test.shape)
    dtrain = lgb.Dataset(x_train, y_train)
    deval = lgb.Dataset(x_test, y_test, reference=dtrain)

    bst = lgb.LGBMClassifier(objective='binary',learning_rate=0.01)
    # # Training with 5-fold CV:
    # lgb.cv(params, dtrain, num_boost_round=20, nfold=5)
    lgb_model = bst.fit(x_train, y_train)
    y_pred = bst.predict(x_test)
    y_pred_prob = bst.predict_proba(x_test)
    print(len(y_pred))
    accuracy = np.mean(y_pred == y_test)
    

    # print(feature_importance)
    return y_pred,y_pred_prob,y_test,accuracy,lgb_model

def eval_model(y_pred,y_pred_prob,y_test):
    df_pred1 = pd.DataFrame()
    df_pred1["pred_binary"] = y_pred
    df_pred1["pred_prob"] = [x[1] for x in y_pred_prob]
    df_pred1["pred_prob_bin"] =  np.where(df_pred1['pred_prob'] > 0.6, 1,0)
    df_pred1["pred_truth"] = y_test
    df_pred2 = df_pred1.dropna()
    df_pred3 = df_pred2[df_pred2["pred_prob_bin"]==1]

    accuracy = np.mean(df_pred3["pred_prob_bin"] == df_pred3["pred_truth"])
    print(f"Decision Tree Accuracy: {accuracy}")
    print(df_pred3.shape)

df_pred_y = ['diff_3_cate']
df2,features,df_pred_y = get_train_df(df_pred_y)
#y_pred,y_pred_prob,y_test,accuracy = r_train_model(df2,features,df_pred_y)
#eval_model(y_pred,y_pred_prob,y_test)

for i in range(0,100):
    y_pred,y_pred_prob,y_test,accuracy,lgb_model = r_train_model(df2,features,df_pred_y)
    save_name = '_'.join(['model',"2022_2024",str(i),str(int(accuracy*100))])+'.txt'
    save_dir1 = os.path.join(ProjectDir().model_dir,"lgb_pred_return",save_name)
    print(save_dir1)
    lgb_model.booster_.save_model(save_dir1)



