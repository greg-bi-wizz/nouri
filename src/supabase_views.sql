-- ============================================================================
-- NourishBox Supabase Views (CSV-Compatible)
-- ============================================================================
--
-- This file creates views that work with data imported from CSV files.
-- CSV imports store dates as TEXT, so we use explicit type casting.
--
-- Run this AFTER importing your CSV data to Supabase.
-- ============================================================================

-- Drop existing views if they exist
DROP VIEW IF EXISTS v_active_customers;
DROP VIEW IF EXISTS v_monthly_revenue;
DROP VIEW IF EXISTS v_customer_lifetime_value;
DROP VIEW IF EXISTS v_product_popularity;
DROP VIEW IF EXISTS v_churn_summary;

-- ============================================================================
-- VIEWS for Common Queries
-- ============================================================================

-- Active customer summary
CREATE OR REPLACE VIEW v_active_customers AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.registration_date::DATE,
    c.acquisition_channel,
    s.subscription_id,
    s.plan_name,
    s.monthly_price::DECIMAL(10,2),
    s.start_date::DATE,
    CURRENT_DATE - s.start_date::DATE AS days_active
FROM customers c
JOIN subscriptions s ON c.customer_id = s.customer_id
WHERE s.status = 'active';

-- Monthly revenue summary
CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT
    year_month,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_orders,
    SUM(order_total::DECIMAL) AS total_revenue,
    AVG(order_total::DECIMAL) AS avg_order_value,
    SUM(CASE WHEN delivery_status = 'delivered'
        THEN order_total::DECIMAL ELSE 0 END) AS delivered_revenue,
    COUNT(CASE WHEN delivery_status = 'delivered' THEN 1 END) AS delivered_orders
FROM orders
GROUP BY year_month
ORDER BY year_month;

-- Customer lifetime value
CREATE OR REPLACE VIEW v_customer_lifetime_value AS
SELECT
    c.customer_id,
    c.registration_date::DATE,
    c.acquisition_channel,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.order_total::DECIMAL), 0) AS total_revenue,
    COALESCE(AVG(o.order_total::DECIMAL), 0) AS avg_order_value,
    CURRENT_DATE - c.registration_date::DATE AS days_since_registration,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM subscriptions s2
            WHERE s2.customer_id = c.customer_id
            AND s2.status = 'active'
        ) THEN TRUE
        ELSE FALSE
    END AS is_active
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.registration_date, c.acquisition_channel;

-- Product popularity
CREATE OR REPLACE VIEW v_product_popularity AS
SELECT
    product_type,
    product_name,
    product_category,
    COUNT(*) AS times_ordered,
    SUM(quantity::INTEGER) AS total_quantity,
    AVG(unit_cost::DECIMAL) AS avg_cost
FROM order_items
GROUP BY product_type, product_name, product_category
ORDER BY times_ordered DESC;

-- Churn summary by reason
CREATE OR REPLACE VIEW v_churn_summary AS
SELECT
    churn_reason,
    COUNT(*) AS churn_count,
    ROUND(AVG(subscription_length_days::INTEGER), 0) AS avg_days_before_churn,
    SUM(CASE WHEN attempted_retention::BOOLEAN THEN 1 ELSE 0 END) AS retention_attempts,
    SUM(CASE WHEN retention_offer_accepted::BOOLEAN THEN 1 ELSE 0 END) AS retention_successes,
    CASE
        WHEN SUM(CASE WHEN attempted_retention::BOOLEAN THEN 1 ELSE 0 END) > 0
        THEN ROUND(
            100.0 * SUM(CASE WHEN retention_offer_accepted::BOOLEAN THEN 1 ELSE 0 END) /
            SUM(CASE WHEN attempted_retention::BOOLEAN THEN 1 ELSE 0 END), 2
        )
        ELSE 0
    END AS retention_success_rate
FROM churn_events
GROUP BY churn_reason
ORDER BY churn_count DESC;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Test the views (run these to verify)
/*

-- View 1: Active customers
SELECT * FROM v_active_customers LIMIT 10;

-- View 2: Monthly revenue
SELECT * FROM v_monthly_revenue ORDER BY year_month DESC LIMIT 12;

-- View 3: Top customers by lifetime value
SELECT * FROM v_customer_lifetime_value
ORDER BY total_revenue DESC
LIMIT 10;

-- View 4: Most popular products
SELECT * FROM v_product_popularity LIMIT 10;

-- View 5: Churn analysis
SELECT * FROM v_churn_summary;

*/

-- ============================================================================
-- USEFUL QUERIES (Copy-paste ready)
-- ============================================================================

-- Total revenue
/*
SELECT SUM(order_total::DECIMAL) as total_revenue
FROM orders;
*/

-- Active vs Churned breakdown
/*
SELECT
    status,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM subscriptions
GROUP BY status
ORDER BY count DESC;
*/

-- Revenue by subscription plan
/*
SELECT
    s.plan_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.order_total::DECIMAL) as total_revenue,
    AVG(o.order_total::DECIMAL) as avg_order_value
FROM subscriptions s
JOIN orders o ON s.subscription_id = o.subscription_id
GROUP BY s.plan_name
ORDER BY total_revenue DESC;
*/

-- Churn rate by acquisition channel
/*
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT ch.customer_id) AS churned_customers,
    ROUND(100.0 * COUNT(DISTINCT ch.customer_id) /
          NULLIF(COUNT(DISTINCT c.customer_id), 0), 2) AS churn_rate
FROM customers c
LEFT JOIN churn_events ch ON c.customer_id = ch.customer_id
GROUP BY c.acquisition_channel
ORDER BY churn_rate DESC;
*/

-- Average rating by plan
/*
SELECT
    s.plan_name,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating::INTEGER), 2) AS avg_rating,
    ROUND(AVG(r.meal_quality_rating::INTEGER), 2) AS avg_meal_rating,
    ROUND(AVG(r.beauty_quality_rating::INTEGER), 2) AS avg_beauty_rating
FROM reviews r
JOIN subscriptions s ON r.subscription_id = s.subscription_id
GROUP BY s.plan_name
ORDER BY avg_rating DESC;
*/

-- Monthly subscriber growth
/*
SELECT
    DATE_TRUNC('month', registration_date::DATE) AS month,
    COUNT(*) AS new_subscribers,
    SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', registration_date::DATE)) AS cumulative_subscribers
FROM customers
GROUP BY DATE_TRUNC('month', registration_date::DATE)
ORDER BY month;
*/

-- Top 10 customers by revenue
/*
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.order_total::DECIMAL) AS lifetime_value,
    MAX(o.order_date::DATE) AS last_order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.delivery_status = 'delivered'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY lifetime_value DESC
LIMIT 10;
*/

-- Cohort retention analysis (simplified)
/*
SELECT
    DATE_TRUNC('month', registration_date::DATE) AS cohort_month,
    COUNT(*) AS cohort_size,
    SUM(CASE
        WHEN EXISTS (
            SELECT 1 FROM subscriptions s
            WHERE s.customer_id = c.customer_id
            AND s.status = 'active'
        ) THEN 1 ELSE 0
    END) AS still_active,
    ROUND(100.0 * SUM(CASE
        WHEN EXISTS (
            SELECT 1 FROM subscriptions s
            WHERE s.customer_id = c.customer_id
            AND s.status = 'active'
        ) THEN 1 ELSE 0
    END) / COUNT(*), 2) AS retention_rate
FROM customers c
GROUP BY cohort_month
ORDER BY cohort_month;
*/

-- ============================================================================
-- COMMENTS ON VIEWS
-- ============================================================================

COMMENT ON VIEW v_active_customers IS 'Currently active customers with subscription details';
COMMENT ON VIEW v_monthly_revenue IS 'Revenue metrics aggregated by month';
COMMENT ON VIEW v_customer_lifetime_value IS 'Customer lifetime value and engagement metrics';
COMMENT ON VIEW v_product_popularity IS 'Product rankings by order volume';
COMMENT ON VIEW v_churn_summary IS 'Churn analysis by reason with retention metrics';

-- ============================================================================
-- End of Supabase Views
-- ============================================================================

-- ✅ Views created successfully!
-- Run verification queries to test the views.

-- Quick verification:
-- SELECT * FROM v_active_customers LIMIT 5;
