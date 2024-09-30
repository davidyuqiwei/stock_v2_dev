# -*- coding: utf-8 -*-            
# @Time : 2023/8/29 22:41
# @Author: Davidyu
# @FileName: owner_sina.py
from scripts_stock.cfg.set_dir import *
import pandas as pd
from scripts_stock.data_base.get_table_info import GetDataFromDB
from scripts_stock.data_base.insert_into_db import insert_df_to_db


class OnwerIncrease(ProjectDir):
    def __init__(self,ProjectDir):
        self.onwer_increase_save_dir = os.path.join(ProjectDir.analysis_data_dir,"sina_owner_increase.csv")
        self.period1 = "2024-03-31" 
        self.period2  = "2024-06-30"

    def get_increase_data(self,df1,quater_end1,quater_end2):
        df1 = df1[(df1["update_date"]==quater_end1) | (df1["update_date"]==quater_end2)].drop_duplicates()
        #print(df1)

        # 统计 'value' 列中每个唯一值的数量
        value_counts = df1['stock_name'].value_counts()
        # 筛选出计数大于等于3的唯一值
        unique_values_with_more_than_two = value_counts[value_counts >= 2].index.tolist()
        # 使用这些唯一值来过滤原始 DataFrame
        filtered_df = df1[df1['stock_name'].isin(unique_values_with_more_than_two)]

        last_two_dates = filtered_df.groupby('stock_name')['update_date'].apply(lambda x: x.sort_values().tail(3)).reset_index(name='update_date')
        #print(last_two_dates[last_two_dates["stock_name"]=="通化东宝"])

        merged_df = df1.merge(last_two_dates,on=['stock_name', 'update_date'], how='inner')
        #print(merged_df)
        result = merged_df.pivot(index='stock_name', columns='update_date', values='hold_num').reset_index()
        result["diff"] =  result[quater_end2]- result[quater_end1]
        result_increase = result[result["diff"]>0]
        result_increase["owner_name"] = df1["owner_name"].values[0]
        #print(result_increase[["stock_name",quater_end1,quater_end2,"diff"]].sort_values("diff",ascending=False))

        result_decrease = result[result["diff"]<0]
        result_decrease["owner_name"] = df1["owner_name"].values[0]
        #print(result_decrease[["stock_name",quater_end1,quater_end2,"diff"]].sort_values("diff"))
        return result_increase,result_decrease

    def main_run(self):
        df1 = GetDataFromDB.get_sina_onwer_all_df()
        quater_end1 = self.period1
        quater_end2 = self.period2
        df_list = []
        for index,group in df1.groupby("owner_name"):
            a1_in,a1_de = self.get_increase_data(group,quater_end1,quater_end2)
            df_list.append(a1_in)

        df2 = pd.concat(df_list).reset_index()
        df3 = df2[df2.columns[1:]]
        df3.round(3).to_csv(self.onwer_increase_save_dir,index=0)  # type: ignore
        return self

    def insert_index_data2db(self):
        insert_df_to_db(self.onwer_increase_save_dir,"t_sina_owner_increase")


if __name__ == '__main__':
    OnwerIncrease(ProjectDir).main_run().insert_index_data2db()
    



from scripts_stock.utils.common import CommonScript
conn = CommonScript.connect_to_db("test.db")

input_sql_str = """
select t1.*,t2.stock_index,t3.avg_close,t3.avg_close*diff as incease_cash
from t_sina_owner_increase t1
join prd_t_all_stock_index_name t2
on t1.stock_name=t2.stock_name
left join 
(
  select stock_index,avg(close) as avg_close
  from prd_t_fuquan_dfcf
  where date>='2024-06-01' and date<="2024-06-30" 
  group by stock_index
) t3
on t2.stock_index=t3.stock_index
"""
df1 = pd.read_sql_query(input_sql_str, conn)


df2 = df1.dropna().sort_values("incease_cash",ascending=False)
df2.to_csv(os.path.join(project_dir.analysis_data_dir,"owner_sina_increase_out.csv"),index=0,encoding="utf-8-sig")