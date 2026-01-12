# Supabase Troubleshooting Guide

Common issues and solutions when working with NourishBox data in Supabase.

---

## 🐛 Common Errors & Solutions

### Error: "function pg_catalog.extract(unknown, integer) does not exist"

**Problem:** The original `database_schema.sql` was designed for a proper database where dates are stored as DATE type. When importing from CSV, Supabase stores dates as TEXT.

**Solution:** Use the Supabase-specific views file instead!

```sql
-- ❌ DON'T use this for Supabase CSV imports:
-- database_schema.sql (views section has type issues)

-- ✅ USE this instead:
-- supabase_views.sql (has proper type casting)
```

**Steps:**
1. Import your CSV files first (using Table Editor)
2. Then run: `supabase_views.sql`
3. Views will work correctly with TEXT date columns

---

## 📋 Correct Setup Order for Supabase

### Option A: Import CSV Files Directly (Recommended)

This is the easiest way for portfolio projects:

```bash
1. Upload CSV files via Supabase Table Editor
   → Table Editor → Import Data from CSV
   → Repeat for all 9 files

2. Run the views SQL
   → SQL Editor → New Query
   → Paste contents of supabase_views.sql
   → Run

3. Test
   → SELECT * FROM v_active_customers LIMIT 10;
```

### Option B: Use Python Sync Script (Automated)

```bash
1. Setup credentials
   python sync_to_supabase.py --setup
   # Edit .env file

2. Sync data
   python sync_to_supabase.py --clear

3. Create views
   # In Supabase SQL Editor, run supabase_views.sql
```

**Note:** The Python script creates tables automatically but doesn't create views.

---

## 🔧 Fixing Type Issues

### Problem: Dates stored as TEXT

When you import CSV files, date columns are TEXT by default.

**Check your column types:**
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'customers';
```

**If you see TEXT for date columns, you have two options:**

#### Option 1: Cast in queries (Easy - Recommended)
```sql
-- Cast TEXT to DATE when querying
SELECT registration_date::DATE
FROM customers;

-- Or use TO_DATE if needed
SELECT TO_DATE(registration_date, 'YYYY-MM-DD')
FROM customers;
```

This is what `supabase_views.sql` does automatically.

#### Option 2: Alter table structure (Advanced)
```sql
-- Change column type from TEXT to DATE
ALTER TABLE customers
ALTER COLUMN registration_date TYPE DATE
USING registration_date::DATE;

-- Repeat for all date columns
ALTER TABLE orders
ALTER COLUMN order_date TYPE DATE
USING order_date::DATE;

-- etc...
```

**Warning:** Only do Option 2 if you're comfortable with SQL. Option 1 is safer!

---

## 🔍 Verification Queries

After importing data, run these to verify everything is correct:

### Check record counts
```sql
SELECT
    'customers' as table_name,
    COUNT(*) as row_count
FROM customers
UNION ALL
SELECT 'subscriptions', COUNT(*) FROM subscriptions
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'churn_events', COUNT(*) FROM churn_events
UNION ALL
SELECT 'customer_preferences', COUNT(*) FROM customer_preferences
UNION ALL
SELECT 'marketing_campaigns', COUNT(*) FROM marketing_campaigns
UNION ALL
SELECT 'product_catalog', COUNT(*) FROM product_catalog;
```

**Expected results:**
- customers: 2,500
- subscriptions: 2,701
- orders: 32,514
- order_items: 444,979
- reviews: 12,252
- churn_events: 724
- customer_preferences: 2,500
- marketing_campaigns: 70
- product_catalog: 37

### Check data types
```sql
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name IN ('customers', 'orders', 'subscriptions')
ORDER BY table_name, ordinal_position;
```

### Test date casting
```sql
-- This should work without errors
SELECT
    customer_id,
    registration_date::DATE,
    CURRENT_DATE - registration_date::DATE as days_since_reg
FROM customers
LIMIT 10;
```

---

## 💡 Best Practices for Supabase

### 1. Import Order Matters

Import tables in this order to avoid foreign key issues:
1. customers
2. customer_preferences
3. product_catalog
4. marketing_campaigns
5. subscriptions
6. churn_events
7. orders
8. order_items
9. reviews

**Or** just import without foreign keys (they're not critical for analysis).

### 2. Use Views for Complex Queries

Instead of writing complex queries repeatedly, use the views:

```sql
-- ❌ Complex query every time
SELECT c.customer_id, SUM(o.order_total)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- ✅ Use the view
SELECT * FROM v_customer_lifetime_value
ORDER BY total_revenue DESC;
```

### 3. Test in SQL Editor First

Before connecting Power BI:
1. Run verification queries
2. Test the views
3. Make sure dates cast correctly
4. Then connect Power BI

### 4. Index for Performance (Optional)

If queries are slow, add indexes:

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_subscriptions_customer ON subscriptions(customer_id);
```

---

## 🔌 Power BI Connection Issues

### Issue: Can't connect to Supabase

**Check:**
1. ✅ Host format: `db.xxxxx.supabase.co` (no https://, no port in host field)
2. ✅ Port: `5432` (in separate port field if available)
3. ✅ Database: `postgres` (lowercase)
4. ✅ Username: `postgres` (lowercase)
5. ✅ Password: Correct from Supabase settings
6. ✅ SSL/TLS: Enabled (usually automatic)

**Try:**
- Use full connection string format: `db.xxxxx.supabase.co:5432`
- Enable "Encrypt connection" if prompted
- Use Import mode instead of DirectQuery

### Issue: Tables load but relationships are wrong

**Fix in Power BI:**
1. Go to Model view
2. Delete auto-created relationships
3. Manually create:
   - customers[customer_id] → subscriptions[customer_id]
   - customers[customer_id] → orders[customer_id]
   - subscriptions[subscription_id] → orders[subscription_id]
   - orders[order_id] → order_items[order_id]

### Issue: Dates don't work in Power BI

**If dates are imported as TEXT:**

In Power BI Query Editor:
1. Select the date column
2. Transform → Data Type → Date
3. Or use: `= Date.From([registration_date])`

---

## 📊 Common Query Errors

### Error: "column does not exist"

**Cause:** Case sensitivity or typo

**Fix:**
```sql
-- ❌ Wrong case
SELECT Customer_ID FROM customers;

-- ✅ Correct (lowercase)
SELECT customer_id FROM customers;
```

### Error: "operator does not exist: text + integer"

**Cause:** Type mismatch (trying to do math on TEXT)

**Fix:**
```sql
-- ❌ Wrong
SELECT order_total + 10 FROM orders;

-- ✅ Cast first
SELECT order_total::DECIMAL + 10 FROM orders;
```

### Error: "column reference is ambiguous"

**Cause:** Same column name in multiple tables

**Fix:**
```sql
-- ❌ Ambiguous
SELECT customer_id
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- ✅ Use table alias
SELECT c.customer_id
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

---

## 🆘 Quick Fixes

### Reset Everything and Start Fresh

If things are really messed up:

```sql
-- 1. Drop all views
DROP VIEW IF EXISTS v_active_customers CASCADE;
DROP VIEW IF EXISTS v_monthly_revenue CASCADE;
DROP VIEW IF EXISTS v_customer_lifetime_value CASCADE;
DROP VIEW IF EXISTS v_product_popularity CASCADE;
DROP VIEW IF EXISTS v_churn_summary CASCADE;

-- 2. Drop all tables (WARNING: deletes data!)
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS churn_events CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS customer_preferences CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS marketing_campaigns CASCADE;
DROP TABLE IF EXISTS product_catalog CASCADE;

-- 3. Re-import CSVs via Table Editor
-- 4. Run supabase_views.sql
```

### Re-sync from Python

```bash
# Fresh import (clears old data)
python sync_to_supabase.py --clear
```

---

## ✅ Success Checklist

Before moving on to Power BI, verify:

- [ ] All 9 tables visible in Supabase Table Editor
- [ ] Row counts match expected values
- [ ] This query works: `SELECT COUNT(*) FROM customers;` → 2,500
- [ ] This query works: `SELECT SUM(order_total::DECIMAL) FROM orders;` → ~$2.2M
- [ ] Views created successfully: `SELECT * FROM v_active_customers LIMIT 5;`
- [ ] No errors in SQL Editor
- [ ] Can see data in Table Editor for each table

---

## 📚 Useful Supabase Features

### SQL Editor Auto-complete

Supabase SQL Editor has auto-complete:
- Type table name and press Tab
- Shows column suggestions
- Validates syntax

### Table Editor Filters

In Table Editor:
- Click column header to sort
- Use filter icon to filter rows
- Great for quick data inspection

### Database Settings

Settings → Database shows:
- Connection string
- Connection pooling settings
- Database size usage
- Reset database password

---

## 🎯 When to Ask for Help

Try these first:
1. Check this troubleshooting guide
2. Run verification queries
3. Check Supabase status: status.supabase.com
4. Review error message carefully

If still stuck:
- Supabase Discord: supabase.com/discord
- GitHub Issues: github.com/supabase/supabase/issues
- Docs: supabase.com/docs

---

**Most issues are type casting problems!** Use `supabase_views.sql` and you'll be fine. 👍
