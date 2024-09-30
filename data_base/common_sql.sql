>sqlite3
SELECT name FROM sqlite_master  
WHERE type='table'
;



.schema prd_t_fuquan_dfcf


select * from prd_t_owner_sina limit 10;


sqlite3
.open test.db


  stock_name  hold_num  hold_ratio stock_type update_date          owner_name                 update_time
0       通化东宝  36391629        1.83      流通A股,  2024-03-31  sina_owner_abudabi  2024-09-29 21:59:32.651362

 --row_number() over (partition by 1 order by update_date desc) as rank


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

sqlite3 /home/davidyu/vscode/db/test.db <test.sql

select owner_name,stock_name,hold_num from prd_t_owner_sina

from
(
    select * from
    where update_date in (select update_date from tmp_owner_sina_update_date_v1)
) 
group by owner_name,stock_name,hold_num
limit 10
;


  stock_name  2024-03-31  2024-06-30     diff               owner_name                 update_time
0       坤彩科技     7018027     9009694  1991667  sina_owne_merrill_lynch  2024-09-29 22:48:28.243414

select * from prd_t_all_stock_index_name limit 10


select t1.*,t2.stock_index,t3.avg_close 
from t_sina_owner_increase t1
join prd_t_all_stock_index_name t2
on t1.stock_name=t2.stock_name
left join 
(
  select stock_index,avg(close) as avg_close
  from prd_t_fuquan_dfcf
  where date>='2024-06-01' and date<="2024-06-30" and stock_index=601061
  group by stock_index
) t3
on t2.stock_index=t3.stock_index
limit 10
;


  select *
  from prd_t_fuquan_dfcf
  where date>='2024-06-01' and date<="2024-06-30" and stock_index=601061
;


select * from prd_t_owner_sina 
where owner_name='sina_owner_shebao406' and 
update_date in ('2024-06-30','2024-03-31') order by stock_name;
;
