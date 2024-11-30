source ~/.bashrc
cd `dirname $0`
python get_fuquan_index_v2.py
python daily_return.py
python get_fuquan_weekly_price.py

