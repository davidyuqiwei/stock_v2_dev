import sqlite3
from scripts_stock.cfg.set_dir import ProjectDir

class CommonScript:

    @staticmethod
    def connect_to_db(target_db = "test.db"):
        import os 
        conn = sqlite3.connect(os.path.join(ProjectDir.database_dir,target_db))
        return conn