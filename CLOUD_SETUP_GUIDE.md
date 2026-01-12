# Cloud Platform Setup Guide for NourishBox Data

This guide shows you how to host your NourishBox dataset on cloud platforms for free, making it accessible for your portfolio projects.

---

## 🚀 Option 1: Databricks (Enterprise-Level)

**Best for:** Big data analytics, Apache Spark, ML pipelines, enterprise experience
**Free tier:** Community Edition (limited features)
**Time:** 15 minutes

### Setup Steps:

See detailed guide: [DATABRICKS_SETUP.md](DATABRICKS_SETUP.md)

#### Quick Start:
1. Sign up at [community.cloud.databricks.com](https://community.cloud.databricks.com)
2. Create a compute cluster
3. Generate access token
4. Run `python src/sync_to_databricks.py --setup`
5. Edit .env file with your credentials
6. Run `python src/sync_to_databricks.py --clear`

### Portfolio Benefits:
- ✅ "Built Delta Lake data warehouse on Databricks with 485K+ records"
- ✅ "Leveraged Apache Spark for distributed data processing"
- ✅ "Experience with enterprise-grade cloud data platform"
- ✅ Shows big data and modern data engineering skills

---

## 📊 Option 2: Supabase (Quick & Easy)

**Best for:** Power BI, Tableau, API access, SQL queries, web apps
**Free tier:** 500 MB database, unlimited API requests
**Time:** 10 minutes

### Setup Steps:

#### 1. Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email
4. No credit card required ✓

#### 2. Create New Project
1. Click "New Project"
2. Fill in:
   - **Name**: `nourishbox-portfolio`
   - **Database Password**: [create strong password - SAVE THIS!]
   - **Region**: Choose closest to you
3. Click "Create new project"
4. Wait 2-3 minutes for setup

#### 3. Import Your Data

**Method A: Using Table Editor (Easy)**

For each CSV file:
1. Click "Table Editor" in left sidebar
2. Click "Create a new table"
3. Name the table (e.g., `customers`)
4. Click "Import data from CSV"
5. Upload your CSV file
6. Supabase auto-detects columns
7. Click "Save"
8. Repeat for all 9 CSV files

**Method B: Using SQL Editor (Advanced)**

1. Click "SQL Editor" in left sidebar
2. Click "New query"
3. Paste the schema from `database_schema.sql`
4. Run to create tables
5. Import CSV data using the Table Editor import feature

#### 4. Get Connection Details

1. Click "Settings" (gear icon) in sidebar
2. Click "Database"
3. Scroll to "Connection string"
4. Note these details:

```
Host: db.[your-project-ref].supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: [your password from step 2]
```

#### 5. Connect to Power BI

**Option A: Import Mode (Recommended for portfolio)**
1. Open Power BI Desktop
2. Get Data → PostgreSQL database
3. Server: `db.[your-project-ref].supabase.co`
4. Database: `postgres`
5. Data Connectivity mode: Import
6. Click OK
7. Enter credentials:
   - Username: `postgres`
   - Password: [your password]
8. Select tables to import
9. Click "Load"

**Option B: DirectQuery Mode (For live data)**
- Same steps, but choose "DirectQuery" instead of "Import"

#### 6. Test Your Connection

Run this query in Supabase SQL Editor:
```sql
SELECT COUNT(*) FROM customers;
-- Should return 2500

SELECT SUM(order_total) FROM orders;
-- Should return ~2224429.86
```

### Making Your Data Public (Optional)

⚠️ **Only do this if you want the data publicly accessible via API**

1. Go to "Authentication" → "Policies"
2. Enable "Enable Row Level Security" for tables
3. Add policy: "Enable read access for all users"

This allows you to share API endpoints like:
```
https://[your-project-ref].supabase.co/rest/v1/customers
```

### Portfolio Benefits:
- ✅ "Built and deployed PostgreSQL database on Supabase"
- ✅ "Connected cloud database to Power BI for real-time analysis"
- ✅ "Implemented RESTful API for data access"

---

## 🔍 Option 3: Google BigQuery

**Best for:** Enterprise-level experience, large-scale analytics
**Free tier:** 10 GB storage, 1 TB queries/month
**Time:** 15 minutes

### Setup Steps:

#### 1. Create Google Cloud Account
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Sign in with Google account
3. Accept terms of service
4. No credit card required for sandbox mode

#### 2. Create New Project
1. Click project dropdown (top left)
2. Click "New Project"
3. Name: `nourishbox-portfolio`
4. Click "Create"

#### 3. Enable BigQuery
1. Search "BigQuery" in top search bar
2. Click "BigQuery" in results
3. Click "Enable API" if prompted

#### 4. Create Dataset
1. In BigQuery console, click your project name
2. Click "Create Dataset"
3. Fill in:
   - **Dataset ID**: `nourishbox`
   - **Location**: US (multi-region)
   - **Default table expiration**: Never
4. Click "Create dataset"

#### 5. Upload CSV Files

For each CSV file:
1. Click on `nourishbox` dataset
2. Click "Create Table"
3. Fill in:
   - **Source**: Upload
   - **Select file**: [browse to your CSV]
   - **File format**: CSV
   - **Table name**: customers (etc.)
   - **Schema**: Auto detect ✓
4. Click "Create table"
5. Wait for upload
6. Repeat for all 9 files

#### 6. Test Your Data

Click "Compose new query" and run:
```sql
SELECT COUNT(*) as total_customers
FROM `nourishbox-portfolio.nourishbox.customers`;

SELECT
  SUM(order_total) as total_revenue,
  AVG(order_total) as avg_order_value
FROM `nourishbox-portfolio.nourishbox.orders`;
```

#### 7. Connect to Power BI

1. Power BI Desktop → Get Data
2. Search for "Google BigQuery"
3. Sign in with your Google account
4. Select your project: `nourishbox-portfolio`
5. Select dataset: `nourishbox`
6. Select tables to import
7. Click "Load"

### Cost Management:
- Query data in SQL editor (free, counts toward 1 TB/month)
- Use "Query Validator" to see query cost before running
- Storage is free for first 10 GB

### Portfolio Benefits:
- ✅ "Experience with Google Cloud Platform and BigQuery"
- ✅ "Managed 500K+ records in cloud data warehouse"
- ✅ "Optimized SQL queries for distributed computing environment"

---

## 📦 Option 4: Kaggle Datasets (Easiest)

**Best for:** Visibility, community, easy sharing
**Free tier:** Unlimited public datasets
**Time:** 5 minutes

### Setup Steps:

#### 1. Create Kaggle Account
1. Go to [kaggle.com](https://kaggle.com)
2. Sign up (can use Google account)
3. Verify email

#### 2. Create New Dataset
1. Click your profile picture → "Datasets"
2. Click "New Dataset"
3. Click "Upload" or drag files
4. Upload all 9 CSV files
5. Fill in:
   - **Title**: "NourishBox - Subscription Box Business Analytics Dataset"
   - **Subtitle**: "Realistic synthetic data for BI portfolio projects"
   - **Description**: Copy from your README.md

#### 3. Add Metadata
```markdown
# NourishBox Dataset

Comprehensive synthetic dataset for a subscription box service combining healthy meals and beauty products.

## Files
- customers.csv (2,500 rows)
- subscriptions.csv (2,701 rows)
- orders.csv (32,514 rows)
- order_items.csv (444,979 rows)
- reviews.csv (12,252 rows)
- churn_events.csv (724 rows)
- customer_preferences.csv (2,500 rows)
- marketing_campaigns.csv (70 rows)
- product_catalog.csv (37 rows)

## Business Context
NourishBox is a fictional subscription service offering:
- Healthy meal kits (3-5 meals/week)
- Beauty products (4-6 items/month)
- Combo plans

## Key Metrics
- Total Revenue: $2.2M
- Active Subscriptions: 1,776 (71%)
- Churn Rate: 29%
- Average Rating: 4.14/5.0

## Use Cases
- Customer cohort analysis
- Churn prediction modeling
- Marketing ROI analysis
- Product performance tracking
- Revenue forecasting
```

#### 4. Add Tags
- `business intelligence`
- `subscription business`
- `customer analytics`
- `churn analysis`
- `ecommerce`

#### 5. Publish
1. Choose "Public" visibility
2. Click "Create"
3. Share the URL on your resume/LinkedIn!

#### 6. Add SQL Notebook (Optional but Recommended)
1. Click "New Notebook"
2. Choose "SQL" as language
3. Add queries showing interesting insights
4. Publish notebook alongside dataset

Example queries:
```sql
-- Top customers by revenue
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(o.order_total) as lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3
ORDER BY lifetime_value DESC
LIMIT 10;
```

### Portfolio Benefits:
- ✅ "Published dataset on Kaggle with 500K+ records"
- ✅ Easy to share: Just send the link!
- ✅ Community engagement (upvotes, comments)
- ✅ Shows you contribute to data community

---

## 🔗 Option 5: GitHub + Public Repository

**Best for:** Version control, code showcase, developer visibility
**Free tier:** Unlimited public repos
**Time:** 10 minutes

### Setup Steps:

#### 1. Initialize Git Repository
```bash
cd /Users/grzegorz/Library/CloudStorage/OneDrive-Personal/Dokumenty/Work/Szkolenia/my_portfolio_p4_aigen_data

git init
git add .
git commit -m "Initial commit: NourishBox BI project"
```

#### 2. Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Fill in:
   - **Name**: `nourishbox-bi-project`
   - **Description**: "Business Intelligence portfolio project - Subscription box analytics"
   - **Public** ✓
4. Click "Create repository"

#### 3. Push Your Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/nourishbox-bi-project.git
git branch -M main
git push -u origin main
```

#### 4. Add README Badge
Add this to top of your README.md:
```markdown
![Dataset](https://img.shields.io/badge/Dataset-445K%20records-blue)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-green)
```

#### 5. Create GitHub Pages (Optional)
1. Go to repository Settings → Pages
2. Source: Deploy from branch `main`
3. Your project docs will be live at:
   `https://YOUR_USERNAME.github.io/nourishbox-bi-project/`

### Accessing Data:
Anyone can download CSVs directly from GitHub:
```
https://raw.githubusercontent.com/YOUR_USERNAME/nourishbox-bi-project/main/data/nourishbox/customers.csv
```

Or clone entire repo:
```bash
git clone https://github.com/YOUR_USERNAME/nourishbox-bi-project.git
```

### Portfolio Benefits:
- ✅ "Version-controlled data project on GitHub"
- ✅ Shows code quality and documentation skills
- ✅ Easy for recruiters to browse

---

## 🏆 My Recommendations

### For Enterprise/Big Data Roles: Databricks + GitHub
- **Databricks**: Shows big data and Apache Spark skills
- **GitHub**: Version control and code portfolio
- **Resume Impact**: Enterprise-level experience
- **Setup Time**: ~25 minutes

### For BI Analyst Roles: Supabase + Kaggle
- **Supabase**: Easy Power BI connection
- **Kaggle**: Community visibility
- **Resume Impact**: Cloud database + analytics
- **Setup Time**: ~20 minutes

### For Maximum Impact: All Platforms!
- **Databricks**: Enterprise big data platform
- **Supabase**: Quick Power BI integration
- **GitHub**: Code repository
- **Setup Time**: ~40 minutes total

---

## 📋 Connection Strings for Your Portfolio

### Databricks
```
Server Hostname: dbc-xxxxx-yyyy.cloud.databricks.com
HTTP Path: /sql/1.0/warehouses/xxxxx
Catalog: main
Schema: nourishbox
```

### Supabase
```
Host: db.xxxxx.supabase.co
Database: postgres
Port: 5432
SSL: Required
```

### BigQuery
```
Project: nourishbox-portfolio
Dataset: nourishbox
```

### Kaggle
```
https://www.kaggle.com/datasets/YOUR_USERNAME/nourishbox-subscription-analytics
```

### GitHub
```
https://github.com/YOUR_USERNAME/nourishbox-bi-project
```

---

## 🎯 Resume Bullet Point Ideas

**If you use Databricks:**
> "Built Delta Lake data warehouse on Databricks with 485K+ records, leveraging Apache Spark for distributed data processing and advanced analytics on $2.2M subscription business"

**If you use Supabase:**
> "Deployed PostgreSQL database to Supabase cloud platform and connected to Power BI for real-time business intelligence dashboards analyzing $2.2M in subscription revenue"

**If you use BigQuery:**
> "Managed 445K+ records in Google BigQuery data warehouse, implementing SQL queries to analyze customer cohorts, churn patterns, and marketing ROI"

**If you use Kaggle:**
> "Published comprehensive business analytics dataset on Kaggle featuring 9 normalized tables with realistic subscription business metrics"

---

## ❓ Quick Comparison

| Platform | Best For | Difficulty | Portfolio Impact | Power BI | Tech Stack |
|----------|----------|------------|------------------|----------|------------|
| **Databricks** | Big Data/ML | Medium-High | ⭐⭐⭐⭐⭐ | JDBC/ODBC* | Spark/Delta |
| **Supabase** | Live database | Easy | ⭐⭐⭐⭐⭐ | Native | PostgreSQL |
| **BigQuery** | Enterprise | Medium | ⭐⭐⭐⭐⭐ | Native | BigQuery |
| **Kaggle** | Visibility | Very Easy | ⭐⭐⭐⭐ | Download | CSV |
| **GitHub** | Code showcase | Easy | ⭐⭐⭐⭐ | Download | Git |

*Databricks Community Edition may have limited Power BI connector support

---

## 🚀 Next Steps

1. **Choose your platform(s)**:
   - **Databricks** for enterprise/big data experience
   - **Supabase** for quick Power BI connection
   - **Both** for maximum impact!
2. **Follow setup guide**:
   - Databricks: See [DATABRICKS_SETUP.md](DATABRICKS_SETUP.md)
   - Supabase: See [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
3. **Test connection and verify data**
4. **Build your dashboards**
5. **Add to your resume/LinkedIn**

Example LinkedIn updates:

**For Databricks:**
> "Just deployed my BI project to Databricks! 🚀 Built a Delta Lake data warehouse with 485K+ records using Apache Spark. Analyzing subscription business: $2.2M revenue, 2,500 customers across 9 normalized tables. #DataEngineering #Databricks #ApacheSpark #DeltaLake"

**For Supabase:**
> "Just deployed my latest BI project to the cloud! 🚀 Built a comprehensive analytics database on Supabase analyzing subscription business metrics - $2.2M revenue, 2,500 customers, 445K records. Connected to Power BI for interactive dashboards. #DataAnalytics #PowerBI #BusinessIntelligence"

---

Need help with any specific platform setup? Let me know!
