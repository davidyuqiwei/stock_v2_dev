source ~/.bashrc
cd `dirname $0`
python ./to_test_schema/etl_test_v1.py
python ./to_prd_schema/etl_to_prod.py
python ./to_prd_schema/table_drop_duplicates.py