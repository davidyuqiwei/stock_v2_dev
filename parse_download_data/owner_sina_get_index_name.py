from scripts_stock.cfg.set_dir import ProjectDir
import os
import pandas as pd
from scripts_stock.cfg.stock_list import StockList
from scripts_stock.utils.string_process import StringProcess


def get_index_name(project_dir:ProjectDir,stock_lists:StockList,file_name):
    df1 = pd.read_csv(os.path.join(project_dir.download_sample_data_dir,file_name))

    df2 = stock_lists.stock_list_data
    print(df1.head(5))
    print(df2.head(5))

    df3 = df1.merge(df2, on='stock_name',how='left')
    df4 = df3[df1.columns.to_list() + ["stock_index"]].dropna()
    df4["stock_index"] = [StringProcess.int_to_stock_index(x) for x in df4["stock_index"].values.tolist()]
    print(df4.head(5))

if __name__ == '__main__':
    file_list = os.listdir(ProjectDir.download_sample_data_dir)
    for ff in file_list:
        if "sina_owner" in ff:
            print(ff)
            get_index_name(ProjectDir,StockList,ff)


