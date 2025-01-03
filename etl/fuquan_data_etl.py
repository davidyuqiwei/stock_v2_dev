from prd_t_fuquan_dfcf where stock_index = 601985
select stock_index, date, avg(open) as open,
avg(close) as close,
avg(high) as high,
avg(low) as low,
avg(transaction_volume) as transaction_volume
group by stock_index, date