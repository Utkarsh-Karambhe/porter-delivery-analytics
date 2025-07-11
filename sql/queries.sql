CREATE DATABASE porter_db;
USE porter_db;

CREATE TABLE porter_deliveries (
    market_id INT,
    created_at DATETIME,
    actual_delivery_time DATETIME,
    store_id VARCHAR(50),
    store_primary_category VARCHAR(50),
    order_protocol INT,
    total_items INT,
    subtotal FLOAT,
    num_distinct_items INT,
    min_item_price FLOAT,
    max_item_price FLOAT,
    total_onshift_partners INT,
    total_busy_partners INT,
    total_outstanding_orders INT,
    delivery_duration_min FLOAT
);

# 10 Slowest store categories
SELECT store_primary_category, AVG(delivery_duration_min) avg_duration
FROM porter_deliveries
GROUP BY store_primary_category
ORDER BY avg_duration DESC
LIMIT 10;

# Delays by Hour of day
SELECT HOUR(created_at) AS hour_of_day,
COUNT(*) AS total_orders,
ROUND(AVG(delivery_duration_min),2) AS avg_delivery_time
FROM porter_deliveries
GROUP BY hour_of_day
ORDER BY hour_of_day;

# High partner utilization and delays
SELECT *,
(total_busy_partners/total_onshift_partners) AS partner_utilization
FROM porter_deliveries
WHERE (total_busy_partners/total_onshift_partners) > 0.7
AND delivery_duration_min > 60;

# Orders by protocol
SELECT order_protocol, COUNT(*) AS total_orders,
       AVG(delivery_duration_min) AS avg_delivery_time
FROM porter_deliveries
GROUP BY order_protocol
ORDER BY avg_delivery_time DESC;

# Slowest Stores
SELECT store_primary_category, ROUND(AVG(delivery_duration_min),2) AS avg_duration, COUNT(*) AS orders
FROM porter_deliveries
GROUP BY store_primary_category
HAVING COUNT(*) > 100
ORDER BY avg_duration DESC
LIMIT 10;





