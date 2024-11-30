"""

select t1.*,t2.kdjk as weekly_kdjk,t2.macdh as weekly_macdh,t3.stock_name 
from t_stock_kdj_daily_last t1
left join t_stock_kdj_weekly_last t2
on t1.stock_date=t2.stock_date and t1.stock_index=t2.stock_index
left join prd_t_hs300 t3
on t1.stock_index=t3.stock_index
;
"""