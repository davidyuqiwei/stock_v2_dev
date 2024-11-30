from scripts_stock.cfg.db_cfg import DbCfg
from scripts_stock.data_base.test import print_table_test
from scripts_stock.utils.common import CommonScript
from scripts_stock.cfg.set_dir import *
from datetime import datetime
import pandas as pd
from scripts_stock.utils.logging_set import *


dt = datetime.now()


def df_save_to_db(input_df,target_db="test.db",target_table="test"):
    dt = datetime.now()
    print("------------------------")
    print(dt)
    print("------------------------")

    input_df["update_time"] = dt
    conn = CommonScript.connect_to_db(target_db)
    input_df.drop_duplicates().to_sql(target_table, conn, if_exists="replace", index=False)
    conn.close()
    TNLog().info(f"=========== data save to {target_table} =============")
    print_table_test(db=target_db,table_name=target_table)


def fuquan_data_insert_to_db(fuquan_table="prd_t_fuquan_dfcf"):
    try:
        df1 = pd.read_csv(
            os.path.join(ProjectDir.parse_data_dir_fuquan, "fq_all.csv"),
            encoding="utf-8-sig",
        )
        df_save_to_db(df1,target_db="test.db",target_table=fuquan_table)
    except:
        pass
        TNLog().error(f"===========fuquan data cannot save to db =============")



def owner_sina_data_insert_to_db(target_table="prd_t_owner_sina"):
    try:
        df1 = pd.read_csv(
            os.path.join(ProjectDir.parse_data_dir_owner_sina, "owner_sina_combine.csv"),
            encoding="utf-8-sig",
        )
        df_save_to_db(input_df=df1,target_table=target_table)
        TNLog().info(f"===========sina owner data save to db-table prd_t_owner_sina=============")
        print_table_test(db="test.db",table_name="prd_t_owner_sina")
    except Exception as ex:
        TNLog().error(f"===========sina owner data cannot save to db =============")
        print(ex)

def read_db_data(data_dir):
    df1 = pd.read_csv(os.path.join(data_dir),encoding="utf-8-sig")
    return df1

def insert_df_to_db(data_dir,target_table,target_db="test.db",encoding_in="utf-8-sig"):
    try:
        df1 = pd.read_csv(data_dir,encoding=encoding_in)
        df_save_to_db(df1,target_db=target_db,target_table=target_table)
        TNLog().info(f"=========== call insert_df_to_db=============")
        print_table_test(db="test.db",table_name=target_table)
    except Exception as e:
        pass
        TNLog().error(f"==========={data_dir} cannot save to db =============")
        TNLog().error(e)



# def combine_fuquan_data():
#     aa = os.listdir(ProjectDir.download_data_dir_fuquan)
#     csv_list = [x for x in aa if ".csv" in x ]
#     df_list = []
#     for csv_file in csv_list:
#         df1 = pd.read_csv(os.path.join(ProjectDir.download_data_dir_fuquan,csv_file))
#         df_list.append(df1)
#     df2 = pd.concat(df_list)
#     print(df2)


if __name__ == "__main__":
    print("aaa")
    #fuquan_data_insert_to_db(DbCfg.fuquan_db_dfcf)
    #owner_sina_data_insert_to_db()
