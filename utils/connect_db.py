import sqlite3
from scripts_stock.cfg.set_dir import *


class DBprocess:

    @staticmethod
    def connect_db(target_db = "test.db"):
        #target_db = "test.db"

        conn = sqlite3.connect(target_db)
        return conn
    
    @staticmethod
    def insert_to_db(input_df,target_db="test.db"):
        #df1 = pd.read_csv(self.owner_sina_comb_file)
        conn = DBprocess.connect_db( os.path.join(ProjectDir.database_dir,target_db))
        table_name = "prd_t_owner_sina"
        input_df.to_sql(table_name,conn,if_exists='replace',index=False)
        print(f"=============== insert to {target_db}.{table_name} ====================")