# Databricks Setup Guide - NourishBox Data

This guide shows you how to sync your NourishBox data to Databricks and connect it to Power BI.

## 🎯 What You'll Get

- ✅ Enterprise-grade cloud data platform (free Community Edition)
- ✅ Delta Lake tables for reliable data storage
- ✅ Spark SQL for advanced analytics
- ✅ Power BI connection via JDBC/ODBC
- ✅ Notebook-based data exploration
- ✅ Professional portfolio showcase

---

## 📋 Prerequisites

1. Generated CSV data (run `python src/generate_nourishbox_data.py` first)
2. Databricks Community Edition account (free - no credit card required)
3. Python dependencies installed

---

## 🚀 Step-by-Step Setup

### Step 1: Install Required Packages

```bash
# Activate your virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install Databricks dependencies
pip install databricks-sql-connector databricks-connect python-dotenv pandas
```

### Step 2: Create Databricks Account

1. **Go to [community.cloud.databricks.com](https://community.cloud.databricks.com)**
   - Click "Sign up"
   - Choose "Community Edition" (FREE)
   - Sign up with email or Google
   - No credit card required ✓

2. **Verify your email**
   - Check your inbox for verification email
   - Click the verification link
   - Complete your profile

3. **Access your workspace**
   - You'll be redirected to your Databricks workspace
   - URL will be: `https://community.cloud.databricks.com/`

### Step 3: Create a Compute Cluster

1. **Click "Compute" in left sidebar**
2. **Click "Create Cluster"**
3. **Configure cluster**:
   - **Cluster name**: `nourishbox-analytics`
   - **Cluster mode**: Single Node
   - **Databricks runtime version**: Choose latest Runtime (e.g., 14.3 LTS)
   - **Node type**: Keep default (small instance for Community Edition)
   - **Terminate after**: 120 minutes of inactivity
4. **Click "Create Cluster"**
5. **Wait 3-5 minutes** for cluster to start (status will show green)

### Step 4: Get Your Connection Details

1. **In your workspace, click your email/username** (top right)
2. **Click "User Settings"**
3. **Go to "Access tokens" tab**
4. **Click "Generate new token"**
   - **Comment**: `nourishbox-sync`
   - **Lifetime**: 90 days (or your preference)
   - **Click "Generate"**
   - ⚠️ **COPY THIS TOKEN!** You won't see it again
   - Save it temporarily in a secure note

5. **Get your Server Hostname and HTTP Path**:
   - Go back to **"Compute"**
   - Click on your **"nourishbox-analytics"** cluster
   - Go to **"Advanced Options"** → **"JDBC/ODBC"** tab
   - Note these values:
     - **Server Hostname**: `dbc-xxxxx-yyyy.cloud.databricks.com`
     - **HTTP Path**: `/sql/1.0/warehouses/xxxxx`

### Step 5: Configure Environment Variables

1. **Create .env file** in your project root:
   ```bash
   touch .env
   ```

2. **Edit .env file** and add your Databricks credentials:
   ```env
   # Databricks Connection Settings
   DATABRICKS_SERVER_HOSTNAME=dbc-xxxxx-yyyy.cloud.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx
   DATABRICKS_ACCESS_TOKEN=dapi1234567890abcdef

   # Database and catalog settings
   DATABRICKS_CATALOG=main
   DATABRICKS_SCHEMA=nourishbox
   ```

   ⚠️ Replace:
   - `dbc-xxxxx-yyyy.cloud.databricks.com` with YOUR hostname
   - `/sql/1.0/warehouses/xxxxx` with YOUR HTTP path
   - `dapi1234567890abcdef` with YOUR access token

3. **Save the file**

### Step 6: Sync Data to Databricks

**First time setup (fresh import):**
```bash
python src/sync_to_databricks.py --clear
```

This will:
1. Connect to Databricks
2. Create schema (database)
3. Upload CSV files to Databricks File System (DBFS)
4. Create Delta Lake tables
5. Load all CSV data
6. Verify the import

**Expected output:**
```
============================================================
NOURISHBOX → DATABRICKS SYNC
============================================================

🔌 Connecting to Databricks...
   Host: dbc-xxxxx-yyyy.cloud.databricks.com
   Catalog: main
   Schema: nourishbox
✅ Connected successfully!

============================================================
CREATING SCHEMA
============================================================
   ✓ Schema 'main.nourishbox' ready

============================================================
UPLOADING CSV FILES TO DBFS
============================================================
📤 Uploading customers.csv → dbfs:/FileStore/nourishbox/customers.csv
   ✓ Uploaded 2,500 rows
   ...

============================================================
CREATING DELTA TABLES
============================================================
📦 Creating table: main.nourishbox.customers
   ✓ Table created with 2,500 rows
   ...

============================================================
VERIFICATION SUMMARY
============================================================
  customers                     :      2,500 rows
  customer_preferences          :      2,500 rows
  subscriptions                 :      2,701 rows
  orders                        :     32,514 rows
  order_items                   :    444,979 rows
  churn_events                  :        724 rows
  reviews                       :     12,252 rows
  marketing_campaigns           :         70 rows
  product_catalog               :         37 rows
============================================================
  TOTAL RECORDS                 :    485,277
============================================================

✅ Sync completed successfully!
```

---

## 🔄 Updating Data

### Regenerate and Update Data

If you modify the generation script or want to refresh data:

```bash
# 1. Generate new data
python src/generate_nourishbox_data.py

# 2. Sync to Databricks (replaces old data)
python src/sync_to_databricks.py --clear
```

### Append New Data (without deleting old)

```bash
# Just adds new records, keeps existing
python src/sync_to_databricks.py
```

---

## 🔍 Verify Data in Databricks

### Using SQL Editor

1. **Click "SQL Editor"** or **"Workspace"** in left sidebar
2. **Click "Create" → "Notebook"**
3. **Name**: `NourishBox Data Exploration`
4. **Language**: SQL
5. **Cluster**: Select your `nourishbox-analytics` cluster
6. **Run these verification queries:**

```sql
-- Check customer count
SELECT COUNT(*) as total_customers FROM main.nourishbox.customers;
-- Should return: 2,500

-- Check total revenue
SELECT
  COUNT(*) as total_orders,
  SUM(order_total) as total_revenue,
  AVG(order_total) as avg_order_value
FROM main.nourishbox.orders;
-- Should return: 32,514 orders, ~$2.2M revenue

-- Check active subscriptions
SELECT
  status,
  COUNT(*) as count
FROM main.nourishbox.subscriptions
GROUP BY status;
-- Should show: active: 1,776, cancelled: 724, upgraded: 201

-- Top customers by revenue
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  SUM(o.order_total) as lifetime_value
FROM main.nourishbox.customers c
JOIN main.nourishbox.orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_value DESC
LIMIT 10;
```

---

## 📊 Connect Power BI

### Method 1: Using Partner Connect (Easiest for Community Edition)

**Note:** Community Edition has limited connector support. You may need to:
1. Export data to CSV from Databricks
2. Use DirectQuery/Import in Power BI with exported data
3. OR upgrade to Databricks SQL (paid) for native Power BI connector

### Method 2: Using ODBC/JDBC Connector (For Paid Databricks)

1. **Install Databricks ODBC Driver**:
   - Download from: [databricks.com/spark/odbc-drivers-download](https://www.databricks.com/spark/odbc-drivers-download)
   - Run installer
   - Follow installation wizard

2. **Open Power BI Desktop**

3. **Get Data**:
   - Home → Get Data → More
   - Search for "Databricks"
   - Select "Databricks"
   - Click "Connect"

4. **Enter Connection Details**:
   - **Server Hostname**: `dbc-xxxxx-yyyy.cloud.databricks.com`
     (from your .env file)
   - **HTTP Path**: `/sql/1.0/warehouses/xxxxx`
     (from your .env file)
   - **Data Connectivity mode**:
     - Choose **Import** (loads data into Power BI - faster)
     - OR **DirectQuery** (queries live database - always fresh)
   - Click "OK"

5. **Enter Credentials**:
   - **Authentication**: Token
   - **Personal Access Token**: (your token from .env file)
   - Click "Connect"

6. **Select Tables**:
   - Expand "main" → "nourishbox"
   - Check all tables:
     - ☑ customers
     - ☑ customer_preferences
     - ☑ subscriptions
     - ☑ orders
     - ☑ order_items
     - ☑ churn_events
     - ☑ reviews
     - ☑ marketing_campaigns
     - ☑ product_catalog
   - Click "Load"

7. **Wait for import** (may take 1-2 minutes for 485K records)

8. **Done!** ✅

### Method 3: Export from Databricks (For Community Edition Users)

If Power BI connector doesn't work with Community Edition:

1. **In Databricks Notebook, run**:
```python
# Export tables as CSV
tables = ['customers', 'subscriptions', 'orders', 'order_items',
          'reviews', 'churn_events', 'customer_preferences',
          'marketing_campaigns', 'product_catalog']

for table in tables:
    df = spark.table(f"main.nourishbox.{table}")
    df.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(f"dbfs:/FileStore/export/{table}")
```

2. **Download CSV files from Databricks UI**
3. **Import into Power BI** from local files

---

## 🧪 Test Your Connection

### Create a Simple Dashboard (if Power BI connector works)

1. **Add a Card visual**:
   - Drag `orders[order_total]` to the card
   - Change to **Sum**
   - Should show: **$2,224,429.86**

2. **Add a Line chart**:
   - X-axis: `orders[order_date]` (by Month)
   - Y-axis: `orders[order_total]` (Sum)
   - Should show revenue trend 2022-2024

3. **Add a Donut chart**:
   - Legend: `subscriptions[plan_name]`
   - Values: `subscriptions[subscription_id]` (Count)
   - Should show distribution across 6 plans

If these work, you're all set! 🎉

---

## 🛠️ Troubleshooting

### Error: "Connection failed"

**Check:**
1. ✅ Is your cluster running? (green status in Databricks)
2. ✅ Is the hostname correct in .env? (no https://, no trailing slash)
3. ✅ Is the HTTP path correct?
4. ✅ Is the access token valid?
5. ✅ Did you save the .env file?

**Test connection:**
```bash
python src/sync_to_databricks.py
```

If you see "✅ Connected successfully!" then credentials are correct.

### Error: "Cluster not running"

**Solution:**
1. Go to Databricks → Compute
2. Click your cluster
3. Click "Start" button
4. Wait 3-5 minutes
5. Retry sync

### Error: "Token expired"

**Solution:**
1. Go to User Settings → Access tokens
2. Generate new token
3. Update .env file with new token
4. Retry

### Error: "Schema does not exist"

The script creates the schema automatically, but if you see this error:
```sql
-- Run in Databricks SQL Editor:
CREATE SCHEMA IF NOT EXISTS main.nourishbox;
```

### Power BI can't connect (Community Edition)

**Community Edition limitations:**
- May not support all connectors
- ODBC/JDBC might be restricted

**Workarounds:**
1. Use Method 3 (Export to CSV)
2. Upgrade to Databricks SQL Starter ($0.22/DBU - pay as you go)
3. Use Databricks notebooks for analysis instead

---

## 📈 Usage Patterns

### Daily Development

```bash
# Make changes to generation script
# Regenerate data
python src/generate_nourishbox_data.py

# Update Databricks
python src/sync_to_databricks.py --clear

# Refresh in Power BI (if connected)
# (Power BI → Home → Refresh)
```

### Adding New Features

1. Modify `src/generate_nourishbox_data.py`
2. Add new CSV file or modify existing
3. Run generator
4. Run sync (it auto-detects new tables)
5. Refresh Power BI or export new tables

---

## 🎯 What to Put on Your Resume

### Sample Bullet Points

> "Deployed data analytics platform on Databricks with 485K+ records using Delta Lake, enabling enterprise-grade business intelligence analysis"

> "Built automated ETL pipeline using Python and Databricks SQL to sync subscription business data, managing 445K+ order records in cloud data warehouse"

> "Created interactive Power BI dashboards connected to Databricks analyzing $2.2M in revenue across 2,500 customer subscriptions"

> "Leveraged Apache Spark and Delta Lake on Databricks for scalable data processing and analytics"

### LinkedIn Post Idea

```
🚀 Just deployed my BI project to Databricks!

Built a comprehensive subscription analytics platform:
• 485K+ records in Delta Lake format
• Cloud-hosted on Databricks Community Edition
• Apache Spark for data processing
• Connected to Power BI for dashboards
• Automated Python sync pipeline

Analyzing:
📊 $2.2M in revenue
👥 2,500 customers
📦 32,514 orders
⭐ 12,252 reviews

Tech stack: Python, Apache Spark, Delta Lake, Databricks, Power BI

This showcases enterprise-level data engineering and analytics skills!

#DataEngineering #Databricks #DeltaLake #PowerBI #ApacheSpark
```

---

## 🔐 Security Notes

### What's in .env file (PRIVATE - don't commit!)

The `.env` file contains your Databricks credentials. It's automatically added to `.gitignore`.

**Never:**
- ❌ Commit .env to Git
- ❌ Share .env publicly
- ❌ Post access tokens on LinkedIn/portfolio

**Safe to share:**
- ✅ Screenshots of dashboards
- ✅ SQL queries (without credentials)
- ✅ Your GitHub repo (without .env)
- ✅ "I use Databricks" (platform name)

### Regenerating Access Token

If you accidentally expose your token:
1. Go to Databricks → User Settings → Access tokens
2. Revoke the exposed token
3. Generate new token
4. Update .env file
5. Re-run sync script

---

## 💡 Advanced: Using Databricks Notebooks

Databricks notebooks are a powerful way to explore and analyze your data!

### Create Analysis Notebook

1. **Workspace → Create → Notebook**
2. **Name**: "NourishBox Analytics"
3. **Language**: Python or SQL
4. **Cluster**: nourishbox-analytics

### Example Python Analysis

```python
# Load data
customers_df = spark.table("main.nourishbox.customers")
orders_df = spark.table("main.nourishbox.orders")

# Show sample data
display(customers_df.limit(10))

# Calculate metrics
from pyspark.sql import functions as F

revenue_by_month = orders_df.groupBy(
    F.date_format("order_date", "yyyy-MM").alias("month")
).agg(
    F.sum("order_total").alias("revenue"),
    F.count("*").alias("order_count")
).orderBy("month")

display(revenue_by_month)

# Create visualizations
# (Databricks has built-in visualization tools!)
```

### Example SQL Analysis

```sql
-- Revenue trend
SELECT
  DATE_TRUNC('month', order_date) as month,
  SUM(order_total) as revenue,
  COUNT(*) as order_count,
  AVG(order_total) as avg_order_value
FROM main.nourishbox.orders
GROUP BY month
ORDER BY month;

-- Customer lifetime value
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name as customer_name,
  c.state,
  SUM(o.order_total) as lifetime_value,
  COUNT(o.order_id) as total_orders
FROM main.nourishbox.customers c
JOIN main.nourishbox.orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, customer_name, c.state
ORDER BY lifetime_value DESC
LIMIT 20;
```

---

## 🆚 Databricks vs Supabase

| Feature | Databricks | Supabase |
|---------|-----------|----------|
| **Best For** | Big data, ML, Spark | Web apps, PostgreSQL |
| **Free Tier** | Community Edition | 500 MB, unlimited API |
| **Power BI** | JDBC/ODBC (paid tiers) | Native PostgreSQL |
| **Learning Curve** | Medium-High | Easy |
| **Resume Impact** | Enterprise/Big Data | Startup/Modern Stack |
| **Data Format** | Delta Lake (Parquet) | PostgreSQL tables |
| **Processing** | Apache Spark | PostgreSQL |
| **Scalability** | Massive (petabytes) | Small-Medium (GB-TB) |

**Choose Databricks if:**
- ✅ You want big data/ML experience
- ✅ Enterprise role target
- ✅ Learning Spark is priority
- ✅ Need scalable analytics

**Choose Supabase if:**
- ✅ You want quick Power BI setup
- ✅ PostgreSQL experience needed
- ✅ Building web apps later
- ✅ Need easy API access

---

## 📚 Next Steps

1. ✅ **Data synced to Databricks**
2. ✅ **Create exploration notebooks**
3. 🎨 **Build SQL queries and visualizations**
4. 📊 **Export to Power BI or build dashboards**
5. 📸 **Take screenshots** for portfolio
6. 📝 **Write a case study** about your insights
7. 🌐 **Publish and share** your work

---

## ✅ Checklist

Before building dashboards:

- [ ] Databricks account created
- [ ] Cluster created and running
- [ ] Access token generated
- [ ] .env file configured with credentials
- [ ] `sync_to_databricks.py` runs successfully
- [ ] All 9 tables visible in Databricks Data Explorer
- [ ] Verification queries return correct counts
- [ ] (Optional) Power BI connects successfully
- [ ] (Optional) Exploration notebook created

---

## 🆘 Need Help?

**Common issues:**
1. Review "Troubleshooting" section above
2. Check your .env file for typos
3. Verify cluster is running (green status)
4. Check access token hasn't expired

**Still stuck?**
- Check Databricks documentation: [docs.databricks.com](https://docs.databricks.com)
- Community forums: [community.databricks.com](https://community.databricks.com)
- Databricks Academy (free courses): [academy.databricks.com](https://academy.databricks.com)

---

**Ready to analyze big data like the pros!** 🎉

Back to: [README.md](README.md) | [CLOUD_SETUP_GUIDE.md](CLOUD_SETUP_GUIDE.md)
