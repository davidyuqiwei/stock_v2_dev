import json
import os
import re

from scripts.cfg.set_dir import *
from scripts.utils.clean_data import CleanData
from scripts.utils.json_to_df import read_txt_file
import pandas as pd


def parse_data_to_df(file_in):
    df1 = read_txt_file(file_in)
    # print(df1)
    dta = re.findall('data":(.*)\\,"count', df1)
    dta1 = dta[0]
    # print(dta1)
    df = pd.read_json(dta1, encoding="utf-8", orient='records')
    df.to_csv(os.path.join(parse_data_dir, "all_owner_data.csv"),index=0)
    return df


if __name__ == '__main__':
    test_file = "../../data/download_sample_data/all_owner.txt"
    parse_data_to_df(test_file)
