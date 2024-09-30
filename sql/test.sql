drop table if exists tmp_owner_sina_update_date_v1;
create table tmp_owner_sina_update_date_v1 as
select update_date
from 
( 
    select update_date,count(distinct stock_name) as stk_cnt from prd_t_owner_sina 
    group by update_date
    having stk_cnt>1000
    order by update_date desc
)
limit 2
;
