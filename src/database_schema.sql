-- ============================================================================
-- NourishBox Database Schema
-- Subscription Box Service - Healthy Meals & Beauty Products
-- ============================================================================
--
-- This schema defines tables for a subscription box business analytics database.
-- Compatible with PostgreSQL, MySQL, and SQLite (with minor adjustments).
--
-- Usage:
--   1. Create a new database: CREATE DATABASE nourishbox;
--   2. Run this schema: psql nourishbox < database_schema.sql
--   3. Import CSV data using COPY commands or your BI tool
-- ============================================================================

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS churn_events CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS customer_preferences CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS marketing_campaigns CASCADE;
DROP TABLE IF EXISTS product_catalog CASCADE;

-- ============================================================================
-- CUSTOMER TABLES
-- ============================================================================

-- Main customer table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    registration_date DATE NOT NULL,
    acquisition_channel VARCHAR(50) NOT NULL,
    age INTEGER CHECK (age >= 18 AND age <= 120),
    gender VARCHAR(30),
    zip_code VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(2),
    referred_by_customer_id VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_referrer FOREIGN KEY (referred_by_customer_id)
        REFERENCES customers(customer_id) ON DELETE SET NULL
);

-- Customer preferences and profile details
CREATE TABLE customer_preferences (
    customer_id VARCHAR(20) PRIMARY KEY,
    dietary_preferences TEXT,
    beauty_preferences TEXT,
    skin_type VARCHAR(20),
    allergies TEXT,
    preferred_meal_time VARCHAR(20),
    household_size INTEGER CHECK (household_size >= 1 AND household_size <= 10),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_pref FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- ============================================================================
-- SUBSCRIPTION TABLES
-- ============================================================================

-- Subscription plans and history
CREATE TABLE subscriptions (
    subscription_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    plan_type VARCHAR(50) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    monthly_price DECIMAL(10, 2) NOT NULL CHECK (monthly_price > 0),
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'cancelled', 'upgraded', 'paused')),
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_sub FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT chk_end_date CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Churn events for cancelled subscriptions
CREATE TABLE churn_events (
    churn_id VARCHAR(20) PRIMARY KEY,
    subscription_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    churn_date DATE NOT NULL,
    subscription_length_days INTEGER NOT NULL CHECK (subscription_length_days >= 0),
    churn_reason VARCHAR(50) NOT NULL,
    attempted_retention BOOLEAN DEFAULT FALSE,
    retention_offer_accepted BOOLEAN DEFAULT FALSE,
    feedback_provided BOOLEAN DEFAULT FALSE,
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_churn_sub FOREIGN KEY (subscription_id)
        REFERENCES subscriptions(subscription_id) ON DELETE CASCADE,
    CONSTRAINT fk_churn_customer FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- ============================================================================
-- ORDER TABLES
-- ============================================================================

-- Monthly orders/boxes
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    subscription_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE,
    order_total DECIMAL(10, 2) NOT NULL CHECK (order_total >= 0),
    delivery_status VARCHAR(20) NOT NULL CHECK (delivery_status IN ('pending', 'delivered', 'delayed', 'cancelled')),
    delivery_address_zip VARCHAR(20),
    shipping_cost DECIMAL(10, 2) DEFAULT 0.00 CHECK (shipping_cost >= 0),
    discount_applied DECIMAL(10, 2) DEFAULT 0.00 CHECK (discount_applied >= 0),
    year_month VARCHAR(7) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_sub FOREIGN KEY (subscription_id)
        REFERENCES subscriptions(subscription_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT chk_delivery_date CHECK (delivery_date IS NULL OR delivery_date >= order_date)
);

-- Product catalog
CREATE TABLE product_catalog (
    product_id VARCHAR(20) PRIMARY KEY,
    product_type VARCHAR(20) NOT NULL CHECK (product_type IN ('meal', 'beauty')),
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    cost_to_company DECIMAL(10, 2) NOT NULL CHECK (cost_to_company > 0),
    calories INTEGER CHECK (calories IS NULL OR calories > 0),
    retail_value DECIMAL(10, 2) CHECK (retail_value IS NULL OR retail_value > 0),
    tags TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Individual items in each order
CREATE TABLE order_items (
    item_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    product_type VARCHAR(20) NOT NULL CHECK (product_type IN ('meal', 'beauty')),
    product_name VARCHAR(200) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_cost DECIMAL(10, 2) NOT NULL CHECK (unit_cost > 0),
    calories INTEGER CHECK (calories IS NULL OR calories > 0),
    retail_value DECIMAL(10, 2) CHECK (retail_value IS NULL OR retail_value > 0),
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_item_order FOREIGN KEY (order_id)
        REFERENCES orders(order_id) ON DELETE CASCADE
);

-- ============================================================================
-- REVIEW TABLE
-- ============================================================================

-- Customer reviews and ratings
CREATE TABLE reviews (
    review_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    subscription_id VARCHAR(20) NOT NULL,
    review_date DATE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_title VARCHAR(200),
    review_text TEXT,
    would_recommend BOOLEAN DEFAULT TRUE,
    meal_quality_rating INTEGER CHECK (meal_quality_rating IS NULL OR (meal_quality_rating >= 1 AND meal_quality_rating <= 5)),
    beauty_quality_rating INTEGER CHECK (beauty_quality_rating IS NULL OR (beauty_quality_rating >= 1 AND beauty_quality_rating <= 5)),
    delivery_rating INTEGER CHECK (delivery_rating IS NULL OR (delivery_rating >= 1 AND delivery_rating <= 5)),
    value_rating INTEGER CHECK (value_rating IS NULL OR (value_rating >= 1 AND value_rating <= 5)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_order FOREIGN KEY (order_id)
        REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_review_customer FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_review_sub FOREIGN KEY (subscription_id)
        REFERENCES subscriptions(subscription_id) ON DELETE CASCADE
);

-- ============================================================================
-- MARKETING TABLE
-- ============================================================================

-- Marketing campaigns
CREATE TABLE marketing_campaigns (
    campaign_id VARCHAR(20) PRIMARY KEY,
    campaign_name VARCHAR(200) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(10, 2) NOT NULL CHECK (budget >= 0),
    target_audience VARCHAR(50),
    offer_type VARCHAR(50),
    offer_value INTEGER CHECK (offer_value >= 0),
    impressions INTEGER DEFAULT 0 CHECK (impressions >= 0),
    clicks INTEGER DEFAULT 0 CHECK (clicks >= 0),
    conversions INTEGER DEFAULT 0 CHECK (conversions >= 0),
    ctr DECIMAL(5, 2) CHECK (ctr >= 0 AND ctr <= 100),
    conversion_rate DECIMAL(5, 2) CHECK (conversion_rate >= 0 AND conversion_rate <= 100),
    cost_per_acquisition DECIMAL(10, 2) CHECK (cost_per_acquisition >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_campaign_dates CHECK (end_date >= start_date),
    CONSTRAINT chk_clicks CHECK (clicks <= impressions),
    CONSTRAINT chk_conversions CHECK (conversions <= clicks)
);

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- Customer indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_registration_date ON customers(registration_date);
CREATE INDEX idx_customers_acquisition_channel ON customers(acquisition_channel);
CREATE INDEX idx_customers_referred_by ON customers(referred_by_customer_id);

-- Subscription indexes
CREATE INDEX idx_subscriptions_customer ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_plan ON subscriptions(plan_type);
CREATE INDEX idx_subscriptions_dates ON subscriptions(start_date, end_date);

-- Order indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_subscription ON orders(subscription_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_year_month ON orders(year_month);
CREATE INDEX idx_orders_delivery_status ON orders(delivery_status);

-- Order items indexes
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product_type ON order_items(product_type);
CREATE INDEX idx_order_items_product_name ON order_items(product_name);

-- Review indexes
CREATE INDEX idx_reviews_customer ON reviews(customer_id);
CREATE INDEX idx_reviews_order ON reviews(order_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_date ON reviews(review_date);

-- Churn indexes
CREATE INDEX idx_churn_customer ON churn_events(customer_id);
CREATE INDEX idx_churn_reason ON churn_events(churn_reason);
CREATE INDEX idx_churn_date ON churn_events(churn_date);

-- Campaign indexes
CREATE INDEX idx_campaigns_type ON marketing_campaigns(campaign_type);
CREATE INDEX idx_campaigns_dates ON marketing_campaigns(start_date, end_date);

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
    c.registration_date,
    c.acquisition_channel,
    s.subscription_id,
    s.plan_name,
    s.monthly_price,
    s.start_date,
    EXTRACT(DAY FROM CURRENT_DATE - s.start_date) AS days_active
FROM customers c
JOIN subscriptions s ON c.customer_id = s.customer_id
WHERE s.status = 'active';

-- Monthly revenue summary
CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT
    year_month,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_orders,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS avg_order_value,
    SUM(CASE WHEN delivery_status = 'delivered' THEN order_total ELSE 0 END) AS delivered_revenue,
    COUNT(CASE WHEN delivery_status = 'delivered' THEN 1 END) AS delivered_orders
FROM orders
GROUP BY year_month
ORDER BY year_month;

-- Customer lifetime value
CREATE OR REPLACE VIEW v_customer_lifetime_value AS
SELECT
    c.customer_id,
    c.registration_date,
    c.acquisition_channel,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.order_total) AS total_revenue,
    AVG(o.order_total) AS avg_order_value,
    EXTRACT(DAY FROM CURRENT_DATE - c.registration_date) AS days_since_registration,
    CASE
        WHEN s.status = 'active' THEN TRUE
        ELSE FALSE
    END AS is_active
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN subscriptions s ON c.customer_id = s.customer_id AND s.status = 'active'
GROUP BY c.customer_id, c.registration_date, c.acquisition_channel, s.status;

-- Product popularity
CREATE OR REPLACE VIEW v_product_popularity AS
SELECT
    product_type,
    product_name,
    product_category,
    COUNT(*) AS times_ordered,
    SUM(quantity) AS total_quantity,
    AVG(unit_cost) AS avg_cost
FROM order_items
GROUP BY product_type, product_name, product_category
ORDER BY times_ordered DESC;

-- Churn summary by reason
CREATE OR REPLACE VIEW v_churn_summary AS
SELECT
    churn_reason,
    COUNT(*) AS churn_count,
    ROUND(AVG(subscription_length_days), 0) AS avg_days_before_churn,
    SUM(CASE WHEN attempted_retention THEN 1 ELSE 0 END) AS retention_attempts,
    SUM(CASE WHEN retention_offer_accepted THEN 1 ELSE 0 END) AS retention_successes,
    CASE
        WHEN SUM(CASE WHEN attempted_retention THEN 1 ELSE 0 END) > 0
        THEN ROUND(100.0 * SUM(CASE WHEN retention_offer_accepted THEN 1 ELSE 0 END) /
                   SUM(CASE WHEN attempted_retention THEN 1 ELSE 0 END), 2)
        ELSE 0
    END AS retention_success_rate
FROM churn_events
GROUP BY churn_reason
ORDER BY churn_count DESC;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE customers IS 'Customer master table with demographics and acquisition data';
COMMENT ON TABLE customer_preferences IS 'Customer dietary and beauty product preferences';
COMMENT ON TABLE subscriptions IS 'Subscription plans and history for each customer';
COMMENT ON TABLE orders IS 'Monthly box orders and delivery information';
COMMENT ON TABLE order_items IS 'Individual products included in each order';
COMMENT ON TABLE reviews IS 'Customer reviews and ratings for delivered orders';
COMMENT ON TABLE churn_events IS 'Cancellation events and retention attempts';
COMMENT ON TABLE marketing_campaigns IS 'Marketing campaign performance metrics';
COMMENT ON TABLE product_catalog IS 'Available meal and beauty products';

-- ============================================================================
-- Sample Queries
-- ============================================================================

/*

-- Find top 10 customers by lifetime value
SELECT * FROM v_customer_lifetime_value
ORDER BY total_revenue DESC
LIMIT 10;

-- Monthly revenue trend
SELECT * FROM v_monthly_revenue
ORDER BY year_month DESC;

-- Churn rate by acquisition channel
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT ch.customer_id) AS churned_customers,
    ROUND(100.0 * COUNT(DISTINCT ch.customer_id) / COUNT(DISTINCT c.customer_id), 2) AS churn_rate
FROM customers c
LEFT JOIN churn_events ch ON c.customer_id = ch.customer_id
GROUP BY c.acquisition_channel
ORDER BY churn_rate DESC;

-- Average rating by subscription plan
SELECT
    s.plan_name,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(AVG(r.meal_quality_rating), 2) AS avg_meal_rating,
    ROUND(AVG(r.beauty_quality_rating), 2) AS avg_beauty_rating
FROM reviews r
JOIN subscriptions s ON r.subscription_id = s.subscription_id
GROUP BY s.plan_name
ORDER BY avg_rating DESC;

-- Marketing campaign ROI
SELECT
    campaign_type,
    COUNT(*) AS num_campaigns,
    SUM(budget) AS total_budget,
    SUM(conversions) AS total_conversions,
    ROUND(AVG(conversion_rate), 2) AS avg_conversion_rate,
    ROUND(AVG(cost_per_acquisition), 2) AS avg_cpa
FROM marketing_campaigns
GROUP BY campaign_type
ORDER BY avg_conversion_rate DESC;

-- Cohort analysis (simplified)
SELECT
    DATE_TRUNC('month', registration_date) AS cohort_month,
    COUNT(*) AS cohort_size,
    SUM(CASE WHEN s.status = 'active' THEN 1 ELSE 0 END) AS still_active,
    ROUND(100.0 * SUM(CASE WHEN s.status = 'active' THEN 1 ELSE 0 END) / COUNT(*), 2) AS retention_rate
FROM customers c
LEFT JOIN subscriptions s ON c.customer_id = s.customer_id AND s.status = 'active'
GROUP BY cohort_month
ORDER BY cohort_month;

*/

-- ============================================================================
-- End of Schema
-- ============================================================================
