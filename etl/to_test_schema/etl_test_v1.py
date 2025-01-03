from scripts_stock.data_base.insert_into_db import insert_df_to_db, df_save_to_db
from scripts_stock.utils.common import CommonScript
import pandas as pd
from scripts_stock.utils.logging_set import *

from scripts_stock.download_data.hs300.download_hs300_daily import *
from scripts_stock.download_data.owner_dfcf.download_owner_dfcf_history import *
from scripts_stock.download_data.financial_report.download_fin_report_history import *
from scripts_stock.download_data.cash_flow.cash_flow_stocks import *

from scripts_stock.etl.to_prd_schema.table_drop_duplicates import deduplicates_one_tables
from scripts_stock.data_base.cfg import DBTableName
from scripts_stock.utils.logging_set import *


class TestDbEtl:
    def __init__(self):
        test_v1 = ''

    def etl_hs300(self):
        hs300_cfg = DownloadHS300(ProjectDir)
        # print(hs300_cfg.tmp_data_txt_name.replace('.txt', '.csv'))
        # hs300_csv = hs300_cfg.tmp_data_txt_name.replace('.txt', '.csv')
        df1 = pd.read_csv(hs300_cfg.final_data_name)
        df_save_to_db(df1, target_table=DBTableName.table_hs300_etf())

    def owner_dfcf(self):
        owner_dfcf_cdg = DownloadOwnerDFCF(ProjectDir)
        file_csv = owner_dfcf_cdg.final_data_name
        print(file_csv)
        df1 = pd.read_csv(file_csv)
        df_save_to_db(df1, target_table=DBTableName.table_owner_dfcf())

    def fin_report(self):
        fin_reprot_cfg = DownloadFinReport(ProjectDir)
        fin_report_csv = fin_reprot_cfg.final_data_name
        df1 = pd.read_csv(fin_report_csv)
        print(df1.head(10))
        df_save_to_db(df1, target_table=DBTableName.table_fin_report())

    def cash_flow_stocks(self):
        cash_flow_stocks_cfg = DownloadCashFlowData(ProjectDir)
        cash_flow_stocks_cfg_csv = cash_flow_stocks_cfg.base_data
        df1 = pd.read_csv(cash_flow_stocks_cfg_csv)
        print(df1.head(10))
        df_save_to_db(df1, target_table=DBTableName.cash_flow_stocks())
    
    def main_run(self):
        self.etl_hs300()
        #self.fin_report()
        self.cash_flow_stocks()
        deduplicates_one_tables(DBTableName.table_hs300_etf())
        deduplicates_one_tables(table_in=DBTableName.table_fin_report())
        deduplicates_one_tables(table_in=DBTableName.cash_flow_stocks())

if __name__ == '__main__':
    try:
        TestDbEtl().main_run()
    except Exception as e:
        TNLog().error("====================================")
        TNLog().error("==== test db etl error ====")
        TNLog().error(e)
        print_exception_info()
        TNLog().error("====================================")
