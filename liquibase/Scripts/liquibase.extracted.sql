--liquibase formatted sql

--changeset JamesBennett:1000 labels:dbt-schema-changes
create or replace view DBT.orders_view as ( select order_id, customer_id, total_amount, order_date, modified_at, case when total_amount > 1000 then 'high_value' else 'regular' end as order_value_type from PUBLIC.orders );
--rollback empty

--changeset JamesBennett:1001 labels:dbt-schema-changes
create or replace transient table DBT.customer_order_summary as ( with orders as ( select order_id, customer_id, total_amount, order_date, modified_at from PUBLIC.orders ), customers as ( select customer_id, customer_name, email, signup_date, country_code, is_active from PUBLIC.customers ), aggregated_orders as ( select o.customer_id, count(*) as order_count, sum(o.total_amount) as total_spent, max(o.order_date) as last_order_date from orders o group by o.customer_id ), recent_orders as ( select o.customer_id, o.order_id, o.order_date, row_number() over ( partition by o.customer_id order by o.order_date desc ) as order_rank from orders o ), final as ( select c.customer_id, c.customer_name, c.email, coalesce(ao.order_count, 0) as order_count, coalesce(ao.total_spent, 0) as total_spent, ao.last_order_date, case when ao.total_spent > 1000 then 'high_value' else 'regular' end as customer_type, ro.order_id as most_recent_order_id from customers c left join aggregated_orders ao on c.customer_id = ao.customer_id left join recent_orders ro on c.customer_id = ro.customer_id and ro.order_rank = 1 ) select * from final ) ;
--rollback empty

--changeset JamesBennett:1002 labels:dbt-schema-changes
drop view if exists DBT.customer_order_summary__dbt_tmp cascade;
--rollback empty

