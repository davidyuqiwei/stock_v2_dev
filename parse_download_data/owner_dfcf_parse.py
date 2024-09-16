import json
import os
import re

from scripts_stock.cfg.set_dir import *
from scripts_stock.utils.clean_data import CleanData
from scripts_stock.utils.json_to_df import read_txt_file
import pandas as pd

from scripts_stock.utils.parse_data import parse_data_to_df


def parse_data_to_df_history(file_in):
    """
    *** Need to update ***
    :param file_in:
    :return:
    """
    for i in range(0,5):
        df1 = read_txt_file(file_in)
        # print(df1)
        dta = re.findall('data":(.*)\\,"count', df1)
        dta1 = dta[0]
        # print(dta1)
        df = pd.read_json(dta1, encoding="utf-8", orient='records')
        df.to_csv(os.path.join(parse_data_dir, "all_owner_data.csv"),index=0)
        return df

if __name__ == '__main__':
    test_file = "../../data/download_sample_data/all_owner_2019-06-30.txt"
    _,_ = parse_data_to_df(test_file,"all_owner_data.csv")
