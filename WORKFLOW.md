# NourishBox Data Workflow - Complete Guide

This document shows the complete workflow from data generation to Power BI dashboards.

---

## 🔄 Complete Workflow

```
1. Generate Data        2. Sync to Cloud       3. Connect Power BI      4. Build Dashboards
   (Local CSV)             (Supabase)            (Live Connection)         (Portfolio)
       ↓                       ↓                       ↓                        ↓
  Python Script  ────→  Cloud Database  ────→  Import to Power BI  ────→   Publish & Share
```

---

## 📋 One-Time Setup (Do Once)

### Step 1: Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install all packages
pip install -r requirements.txt
```

### Step 2: Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Sign up (free, no credit card)
3. Create new project: `nourishbox-portfolio`
4. **Save your database password!** ⚠️

### Step 3: Configure Credentials
```bash
# Create .env template
python sync_to_supabase.py --setup

# Edit .env file with your Supabase credentials
# (Get from: Supabase → Settings → Database)
```

**Edit `.env`:**
```env
SUPABASE_HOST=db.abcdefghijklmnop.supabase.co  # Your actual host
SUPABASE_PASSWORD=your-actual-password          # Your actual password
```

---

## 🚀 Regular Workflow (Repeat as Needed)

### Option A: Fresh Start (Recommended First Time)

```bash
# 1. Generate fresh data
python generate_nourishbox_data.py

# 2. Sync to Supabase (clear old data first)
python sync_to_supabase.py --clear

# 3. Connect Power BI and build dashboards
#    (See SUPABASE_SETUP.md for connection details)
```

### Option B: Update Existing Data

```bash
# 1. Regenerate data
python generate_nourishbox_data.py

# 2. Append new data (keeps old data)
python sync_to_supabase.py

# 3. Refresh in Power BI
#    (Power BI → Home → Refresh)
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  generate_nourishbox_data.py                                │
│         ↓                                                   │
│  data/nourishbox/*.csv (9 files, 485K records)              │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ sync_to_supabase.py
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD (SUPABASE)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PostgreSQL Database                                        │
│    ├─ customers (2,500 rows)                                │
│    ├─ subscriptions (2,701 rows)                            │
│    ├─ orders (32,514 rows)                                  │
│    ├─ order_items (444,979 rows)                            │
│    └─ ... 5 more tables                                     │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ PostgreSQL Connector
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    POWER BI                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Data Model (Import or DirectQuery)                         │
│         ↓                                                   │
│  DAX Measures & Calculations                                │
│         ↓                                                   │
│  Interactive Dashboards                                     │
│         ↓                                                   │
│  Publish to PowerBI.com / Export PDF / Portfolio            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Common Scenarios

### Scenario 1: First Time Setup
```bash
# 1. Generate data
python generate_nourishbox_data.py

# 2. Setup Supabase credentials
python sync_to_supabase.py --setup
# (edit .env file)

# 3. Sync to cloud
python sync_to_supabase.py --clear

# 4. Connect Power BI
# (Use credentials from .env)

# 5. Build dashboards!
```

### Scenario 2: Change Data Parameters
```bash
# 1. Edit generate_nourishbox_data.py
#    - Change NUM_CUSTOMERS
#    - Change date range
#    - Add new products, etc.

# 2. Regenerate
python generate_nourishbox_data.py

# 3. Update cloud
python sync_to_supabase.py --clear

# 4. Refresh Power BI
```

### Scenario 3: Add New Table/Field
```bash
# 1. Modify generation script
#    - Add new CSV generation function
#    - Or add columns to existing tables

# 2. Generate
python generate_nourishbox_data.py

# 3. Sync (auto-detects new tables)
python sync_to_supabase.py --clear

# 4. In Power BI:
#    - Get Data → Refresh
#    - Add new table to model
```

### Scenario 4: Share With Team
```bash
# Option A: Share Supabase credentials
# (Create new user in Supabase with read-only access)

# Option B: Export Power BI report
# (Publish to PowerBI.com or export as PDF)

# Option C: Share GitHub repo
# (They can generate their own Supabase instance)
```

---

## 📁 File Reference

### Data Generation
| File | Purpose |
|------|---------|
| `generate_nourishbox_data.py` | Main data generator script |
| `data/nourishbox/*.csv` | Generated data files (9 files) |

### Cloud Sync
| File | Purpose |
|------|---------|
| `sync_to_supabase.py` | Sync script to upload data to Supabase |
| `.env` | Database credentials (PRIVATE - don't commit!) |
| `.env.example` | Template for credentials |

### Analysis & Visualization
| File | Purpose |
|------|---------|
| `example_analysis.py` | Sample Python analysis |
| `database_schema.sql` | SQL schema with sample queries |
| Power BI file | Your dashboards (create this) |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `PROJECT_SUMMARY.md` | Quick start guide |
| `SUPABASE_SETUP.md` | Detailed Supabase setup instructions |
| `CLOUD_SETUP_GUIDE.md` | All cloud platform options |
| `WORKFLOW.md` | This file - complete workflow |

---

## ⚡ Quick Commands Reference

```bash
# === SETUP (once) ===
pip install -r requirements.txt
python sync_to_supabase.py --setup
# (edit .env file with your credentials)

# === GENERATE DATA ===
python generate_nourishbox_data.py

# === SYNC TO CLOUD ===
# Fresh start (delete old data)
python sync_to_supabase.py --clear

# Append only (keep old data)
python sync_to_supabase.py

# === ANALYSIS ===
# Run sample analysis
python example_analysis.py

# === POWER BI ===
# 1. Open Power BI Desktop
# 2. Get Data → PostgreSQL
# 3. Server: [from .env file]
# 4. Database: postgres
# 5. Load tables
# 6. Build dashboards!
```

---

## 🎯 Development Workflow

### Daily Development Cycle

```bash
# Morning: Start working
source venv/bin/activate

# Make changes to generation script
# ...

# Test locally
python generate_nourishbox_data.py
python example_analysis.py

# Looks good? Sync to cloud
python sync_to_supabase.py --clear

# Open Power BI and refresh data
# (Power BI → Home → Refresh)

# Build/update dashboards
# ...

# End of day: Commit changes
git add .
git commit -m "Updated data generation parameters"
git push

# (Don't commit .env or data/*.csv if using .gitignore)
```

---

## 🔐 Security Best Practices

### What to Keep Private ❌
- `.env` file (database credentials)
- Supabase password
- Database connection strings with credentials

### What You CAN Share ✅
- Generated CSV files (they're synthetic)
- Python scripts (without credentials)
- Power BI reports (exported as PDF)
- SQL queries (without connection details)
- Screenshots of dashboards
- GitHub repository (with .env in .gitignore)

### .gitignore Check
```bash
# Verify .env is ignored
cat .gitignore | grep .env

# Should output: .env
```

---

## 📊 Power BI Connection Details

### Import Mode (Recommended)
```
Connection: PostgreSQL
Server: [your-host]:5432
Database: postgres
Username: postgres
Password: [your-password]
Mode: Import
```

**Pros:**
- ✅ Faster dashboard performance
- ✅ Works offline
- ✅ All Power BI features available

**Cons:**
- ❌ Must refresh to see new data
- ❌ Uses Power BI storage

### DirectQuery Mode (Live Connection)
```
Same as above, but:
Mode: DirectQuery
```

**Pros:**
- ✅ Always shows latest data
- ✅ No data stored in Power BI

**Cons:**
- ❌ Slower performance
- ❌ Some features limited
- ❌ Requires internet connection

### Recommended: Import Mode
For portfolio projects, **Import mode** is better because:
1. Faster performance for demos
2. Works offline at interviews
3. Full feature set for impressive visuals

---

## 🎨 Next Steps After Data Sync

### 1. Verify Data
```sql
-- In Supabase SQL Editor:
SELECT COUNT(*) FROM customers;      -- 2,500
SELECT COUNT(*) FROM orders;         -- 32,514
SELECT SUM(order_total) FROM orders; -- ~$2.2M
```

### 2. Build Power BI Model
- Import all tables
- Create relationships
- Define measures

### 3. Create First Dashboard
Start with Executive Dashboard:
- Total Revenue card
- Active Subscriptions card
- MRR trend line
- Plan distribution pie chart

### 4. Document Your Work
- Take screenshots
- Write case study
- Note key insights
- Prepare presentation

### 5. Publish & Share
- Tableau Public / PowerBI.com
- GitHub repository
- LinkedIn post
- Resume bullet points

---

## 📈 Performance Tips

### For Large Datasets
If you increase `NUM_CUSTOMERS` significantly:

1. **Use batch loading** (already implemented in sync script)
2. **Add indexes** in Supabase:
   ```sql
   CREATE INDEX idx_orders_date ON orders(order_date);
   CREATE INDEX idx_customers_channel ON customers(acquisition_channel);
   ```

3. **Use Power BI aggregations**:
   - Create summary tables for dashboards
   - Use DirectQuery for details

4. **Optimize DAX measures**:
   - Use CALCULATE instead of FILTER
   - Avoid iterators (SUMX, FILTER) on large tables

---

## ✅ Troubleshooting Checklist

Before asking for help, verify:

- [ ] Python virtual environment is activated
- [ ] All dependencies installed (`pip list`)
- [ ] CSV files exist in `data/nourishbox/`
- [ ] `.env` file created and filled out
- [ ] Supabase project is active (check dashboard)
- [ ] Host in .env matches Supabase (no https://)
- [ ] Password in .env is correct
- [ ] Power BI PostgreSQL connector is available
- [ ] Firewall allows PostgreSQL port 5432

Test connection:
```bash
python sync_to_supabase.py
# Should show: "✅ Connected successfully!"
```

---

## 🎓 Learning Path

### Week 1: Foundation
- [x] Generate data locally
- [x] Run example analysis
- [ ] Set up Supabase
- [ ] Sync data to cloud

### Week 2: Power BI Basics
- [ ] Connect Power BI to Supabase
- [ ] Create data model
- [ ] Build simple visuals
- [ ] Create first dashboard

### Week 3: Advanced Analytics
- [ ] DAX measures (MRR, churn rate, CLV)
- [ ] Time intelligence (YoY growth)
- [ ] Customer segmentation
- [ ] Cohort analysis

### Week 4: Portfolio Ready
- [ ] Executive dashboard
- [ ] Churn analysis dashboard
- [ ] Marketing ROI dashboard
- [ ] Documentation & presentation
- [ ] Publish and share

---

## 🌟 Success Criteria

Your portfolio project is ready when:

1. ✅ **Data Quality**
   - 485K+ records in Supabase
   - All tables load correctly
   - Relationships properly defined

2. ✅ **Technical Skills**
   - Python data generation
   - Cloud database deployment
   - Power BI connection
   - DAX measure creation

3. ✅ **Business Value**
   - Clear insights identified
   - Actionable recommendations
   - Professional visualizations
   - Compelling story

4. ✅ **Portfolio Presentation**
   - Published dashboards
   - Documentation complete
   - GitHub repository
   - LinkedIn post

---

## 🚀 You're Ready!

Follow this workflow and you'll have:
- ✅ Cloud-hosted database
- ✅ Professional BI dashboards
- ✅ Portfolio-ready project
- ✅ Resume-worthy experience

**Time investment:**
- Setup: 30 minutes
- First dashboard: 2-3 hours
- Complete portfolio: 1-2 weeks

**Return on investment:**
- Impressive portfolio piece
- Hands-on cloud experience
- Interview conversation starter
- Job opportunities! 🎯

---

**Ready to start?** → Begin with [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

**Need help?** → Check [README.md](README.md) for detailed documentation

**Happy analyzing!** 🎉
