# Supabase Setup Guide - NourishBox Data

This guide shows you how to sync your NourishBox data to Supabase and connect it to Power BI.

## 🎯 What You'll Get

- ✅ Cloud-hosted PostgreSQL database (free)
- ✅ Live Power BI connection
- ✅ SQL query interface
- ✅ Easy data updates (re-run script to refresh)
- ✅ Professional portfolio showcase

---

## 📋 Prerequisites

1. Generated CSV data (run `python generate_nourishbox_data.py` first)
2. Supabase account (free - no credit card)
3. Python dependencies installed

---

## 🚀 Step-by-Step Setup

### Step 1: Install Required Packages

```bash
# Activate your virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install new dependencies
pip install psycopg2-binary python-dotenv
```

### Step 2: Create Supabase Account & Project

1. **Go to [supabase.com](https://supabase.com)**
   - Click "Start your project"
   - Sign up with GitHub (recommended) or email
   - No credit card required ✓

2. **Create New Project**
   - Click "New Project"
   - Organization: (create one if needed)
   - **Project Name**: `nourishbox-portfolio`
   - **Database Password**: Create a strong password
   - ⚠️ **SAVE THIS PASSWORD!** You'll need it later
   - **Region**: Choose closest to you
   - Click "Create new project"
   - Wait 2-3 minutes for provisioning

### Step 3: Get Your Database Credentials

1. In your Supabase project, click **Settings** (gear icon) in sidebar
2. Click **Database** in the Settings menu
3. Scroll to **Connection string** section
4. Note these values:

```
Host: db.abcdefghijklmnop.supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: [the password you created in Step 2]
```

### Step 4: Configure Environment Variables

1. **Create .env file** (Option A - Automatic):
   ```bash
   python sync_to_supabase.py --setup
   ```

   This creates a `.env` template file.

2. **OR create manually** (Option B):
   ```bash
   # Create .env file in your project root
   touch .env
   ```

3. **Edit .env file** and add your credentials:
   ```env
   # Supabase Connection Settings
   SUPABASE_HOST=db.abcdefghijklmnop.supabase.co
   SUPABASE_PASSWORD=your-actual-password-here
   SUPABASE_DB=postgres
   SUPABASE_USER=postgres
   SUPABASE_PORT=5432
   ```

   ⚠️ Replace:
   - `db.abcdefghijklmnop.supabase.co` with YOUR host from Step 3
   - `your-actual-password-here` with YOUR password from Step 2

4. **Save the file**

### Step 5: Sync Data to Supabase

**First time setup (fresh import):**
```bash
python sync_to_supabase.py --clear
```

This will:
1. Connect to Supabase
2. Create all tables
3. Load all CSV data
4. Verify the import

**Expected output:**
```
============================================================
NOURISHBOX → SUPABASE SYNC
============================================================

🔌 Connecting to Supabase...
   Host: db.xxxxx.supabase.co
   Database: postgres
✅ Connected successfully!

============================================================
CREATING TABLES
============================================================
   ✓ Table 'customers' ready
   ✓ Table 'subscriptions' ready
   ...

============================================================
LOADING DATA
============================================================
📤 Loading customers.csv → customers
   ✓ Loaded 2,500 rows
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
python generate_nourishbox_data.py

# 2. Sync to Supabase (replaces old data)
python sync_to_supabase.py --clear
```

### Append New Data (without deleting old)

```bash
# Just adds new records, keeps existing
python sync_to_supabase.py
```

**Note:** The script uses `ON CONFLICT DO NOTHING`, so duplicate IDs won't be inserted twice.

---

## 🔍 Verify Data in Supabase

1. **Go to your Supabase project**
2. **Click "SQL Editor"** in sidebar
3. **Click "New query"**
4. **Run these verification queries:**

```sql
-- Check customer count
SELECT COUNT(*) as total_customers FROM customers;
-- Should return: 4,015

-- Check total revenue
SELECT
  COUNT(*) as total_orders,
  SUM(order_total) as total_revenue,
  AVG(order_total) as avg_order_value
FROM orders;
-- Should return: ~72,799 orders, ~$5.11M revenue

-- Check active subscriptions
SELECT
  status,
  COUNT(*) as count
FROM subscriptions
GROUP BY status;
-- Should show roughly: active ~2,103; cancelled ~1,912; upgraded ~280 (ranges depend on random seed)

-- Top customers by revenue
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  SUM(o.order_total) as lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY lifetime_value DESC
LIMIT 10;
```

---

## 📊 Connect Power BI

### Method 1: PostgreSQL Connector (Recommended)

1. **Open Power BI Desktop**

2. **Get Data**:
   - Home → Get Data → More
   - Search for "PostgreSQL"
   - Select "PostgreSQL database"
   - Click "Connect"

3. **Enter Server Details**:
   - **Server**: `db.abcdefghijklmnop.supabase.co:5432`
     (use YOUR host from .env file)
   - **Database**: `postgres`
   - **Data Connectivity mode**:
     - Choose **Import** (loads data into Power BI - faster)
     - OR **DirectQuery** (queries live database - always fresh)
   - Click "OK"

4. **Enter Credentials**:
   - **User name**: `postgres`
   - **Password**: (your password from .env file)
   - Click "Connect"

5. **Select Tables**:
   - Expand "public" schema
   - Check all tables:
     - ☑ customers
     - ☑ customer_preferences
     - ☑ subscriptions
       - ☑ subscription_monthly
     - ☑ orders
     - ☑ order_items
     - ☑ churn_events
     - ☑ reviews
     - ☑ marketing_campaigns
     - ☑ product_catalog
       - ☑ dim_plan
       - ☑ dim_date
   - Click "Load"

6. **Wait for import** (may take 1-2 minutes for ~1.2M rows total)

7. **Done!** ✅

### Method 2: Native Supabase (Alternative)

Power BI doesn't have a native Supabase connector yet, but PostgreSQL works perfectly since Supabase IS PostgreSQL.

---

## 🔗 Set Up Relationships in Power BI

After loading data, set up these relationships:

1. **Go to Model view** (left sidebar icon)

2. **Create relationships** (drag and drop):

```
customers[customer_id] → subscriptions[customer_id]
customers[customer_id] → orders[customer_id]
customers[customer_id] → customer_preferences[customer_id]
customers[customer_id] → churn_events[customer_id]
customers[customer_id] → reviews[customer_id]
customers[customer_id] → subscription_monthly[customer_id]

subscriptions[subscription_id] → orders[subscription_id]
subscriptions[subscription_id] → reviews[subscription_id]
subscriptions[subscription_id] → churn_events[subscription_id]
subscriptions[subscription_id] → subscription_monthly[subscription_id]

orders[order_id] → order_items[order_id]
orders[order_id] → reviews[order_id]
dim_plan[plan_key] → subscriptions[plan_type]
dim_plan[plan_key] → orders[plan_type_at_order]

dim_date[date_key] → orders[order_date_key]
```

3. **Verify relationships**:
   - All should be **one-to-many** (1:*)
   - Cross-filter direction: **Single** (default)

---

## 🧪 Test Your Connection

### Create a Simple Dashboard

1. **Add a Card visual**:
   - Drag `orders[order_total]` to the card
   - Change to **Sum**
   - Should show: **≈$5,113,660** (will vary slightly with randomness)

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
1. ✅ Is your Supabase project active? (Go to supabase.com)
2. ✅ Is the host correct in .env? (no https://, no trailing slash)
3. ✅ Is the password correct?
4. ✅ Did you save the .env file?

**Test connection:**
```bash
python sync_to_supabase.py
```

If you see "✅ Connected successfully!" then credentials are correct.

### Error: "Table already exists"

No problem! The script handles this. It creates tables only if they don't exist.

To start fresh:
```bash
python sync_to_supabase.py --clear
```

### Error: "No such file or directory: data/nourishbox"

Run data generation first:
```bash
python generate_nourishbox_data.py
```

### Power BI can't connect

**Check:**
1. ✅ Server format: `db.xxxxx.supabase.co:5432` (include port)
2. ✅ Database: `postgres` (lowercase)
3. ✅ Username: `postgres` (lowercase)
4. ✅ Password: (exact match from Supabase)

**Try:**
- Use "Import" mode instead of "DirectQuery"
- Check if SSL is enabled (should be automatic)
- Restart Power BI Desktop

### Data looks wrong in Power BI

**Verify in Supabase first:**
1. Go to Supabase SQL Editor
2. Run: `SELECT COUNT(*) FROM orders;`
3. Should return: 32,514

If Supabase data is correct but Power BI isn't:
- Refresh data: Home → Refresh
- Re-import: Remove tables and load again

---

## 📈 Usage Patterns

### Daily Development

```bash
# Make changes to generation script
# Regenerate data
python generate_nourishbox_data.py

# Update cloud database
python sync_to_supabase.py --clear

# Refresh in Power BI
# (Power BI → Home → Refresh)
```

### Adding New Features

1. Modify `generate_nourishbox_data.py`
2. Add new CSV file or modify existing
3. Run generator
4. Run sync (it auto-detects new tables)
5. Refresh Power BI

### Sharing Your Portfolio

**Database is private by default** - only you can access with credentials.

To share your dashboards:
1. **Publish Power BI report** to PowerBI.com (if you have Pro)
2. **OR** export as PDF and share
3. **OR** record a demo video

**Don't share** your .env file or credentials publicly!

---

## 🎯 What to Put on Your Resume

### Sample Bullet Points

> "Deployed PostgreSQL database to Supabase cloud platform with 485K+ records across 9 normalized tables, enabling real-time business intelligence analysis"

> "Automated ETL pipeline using Python to sync subscription business data to cloud database, refreshing 445K+ order records"

> "Built Power BI dashboards connected to Supabase PostgreSQL database analyzing $2.2M in revenue and 2,500 customer subscriptions"

### LinkedIn Post Idea

```
🚀 Just deployed my latest BI project to the cloud!

Built a comprehensive subscription analytics database:
• 485K+ records across 9 normalized tables
• Cloud-hosted on Supabase (PostgreSQL)
• Connected to Power BI for interactive dashboards
• Automated sync pipeline with Python

Analyzing:
📊 $2.2M in revenue
👥 2,500 customers
📦 32,514 orders
⭐ 12,252 reviews

Tech stack: Python, PostgreSQL, Supabase, Power BI

#DataAnalytics #PowerBI #BusinessIntelligence #CloudComputing
```

---

## 📚 Next Steps

1. ✅ **Data synced to Supabase**
2. ✅ **Power BI connected**
3. 🎨 **Build your first dashboard** (see README.md for ideas)
4. 📸 **Take screenshots** for portfolio
5. 📝 **Write a case study** about your insights
6. 🌐 **Publish and share** your work

---

## 🔐 Security Notes

### What's in .env file (PRIVATE - don't commit!)

The `.env` file contains your database credentials. It's automatically added to `.gitignore`.

**Never:**
- ❌ Commit .env to Git
- ❌ Share .env publicly
- ❌ Post credentials on LinkedIn/portfolio

**Safe to share:**
- ✅ Screenshots of dashboards
- ✅ SQL queries (without credentials)
- ✅ Your GitHub repo (without .env)
- ✅ "I use Supabase" (platform name)

### Resetting Your Password

If you accidentally expose credentials:
1. Go to Supabase → Settings → Database
2. Reset database password
3. Update .env file
4. Re-run sync script

---

## 💡 Advanced: API Access (Optional)

Supabase also provides a REST API to your data!

**Get your API URL:**
1. Supabase → Settings → API
2. Copy "URL" and "anon public" key

**Example API call:**
```bash
curl 'https://abcdefgh.supabase.co/rest/v1/customers?select=*&limit=10' \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

This is useful for:
- Python data analysis
- Web applications
- Mobile apps
- Sharing data with others

---

## ✅ Checklist

Before moving on to Power BI dashboards:

- [ ] Supabase project created
- [ ] .env file configured with credentials
- [ ] `sync_to_supabase.py` runs successfully
- [ ] All 9 tables visible in Supabase Table Editor
- [ ] Verification queries return correct counts
- [ ] Power BI connects successfully
- [ ] All tables loaded in Power BI
- [ ] Relationships created in Model view
- [ ] Test visuals show correct data

---

## 🆘 Need Help?

**Common issues:**
1. Review "Troubleshooting" section above
2. Check your .env file for typos
3. Verify Supabase project is running
4. Test connection with the sync script first

**Still stuck?**
- Check Supabase documentation: [supabase.com/docs](https://supabase.com/docs)
- Power BI community: [community.powerbi.com](https://community.powerbi.com)

---

**Ready to build amazing dashboards!** 🎉

Back to: [README.md](README.md) | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
