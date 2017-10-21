select
    max(b.height),
    to_char(max(b.block_time), 'YYYY-MM-DD HH24:MI:SS')
from blocks b
;

select
	extract(hour from b.block_time) as hour,
	round(avg(b.transactions_count)) as avg_tx_per_block
from blocks b
where extract(year from b.block_time) = 2017
group by hour
order by hour
;

select
	to_char(b.block_time, 'YYYY-MM-DD HH24:MI:SS') as block_time,
	payload->>'_from' as from,
	payload->>'_to'   as to,
	((payload->>'_value')::numeric(64) / power(10, 18)) as value
from logs l
join transactions t on l.transaction_hash = t.transaction_hash
join blocks b on t.block_height = b.height
where lower(l.contract_address) = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
and   l.name = 'Transfer'
order by b.block_time asc
limit 100
;

select
	coalesce(l.payload->>'to', l.payload->>'_to') as receiver,
	count(distinct l.contract_address) as unique_tokens
from logs l
where l.name = 'Transfer'
group by receiver
order by unique_tokens desc
limit 100
;
