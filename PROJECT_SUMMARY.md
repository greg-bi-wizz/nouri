# NourishBox BI Portfolio Project - Quick Start Guide

## 🎯 What You Have

A complete, realistic dataset for a **subscription box business** combining healthy meals and beauty products - perfect for showcasing BI and data analytics skills to potential employers.

## 📦 Project Contents

```
my_portfolio_p4_aigen_data/
├── README.md                          # Full documentation
├── PROJECT_SUMMARY.md                 # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── generate_nourishbox_data.py       # Data generation script
├── example_analysis.py               # Sample analysis code
├── database_schema.sql               # SQL database schema
│
└── data/nourishbox/                  # Generated datasets (9 CSV files)
    ├── customers.csv                 # 2,500 customers
    ├── customer_preferences.csv      # Dietary & beauty preferences
    ├── subscriptions.csv             # 2,701 subscription records
    ├── orders.csv                    # 32,514 monthly orders
    ├── order_items.csv               # 444,979 product line items
    ├── churn_events.csv              # 724 cancellations
    ├── reviews.csv                   # 12,252 customer reviews
    ├── marketing_campaigns.csv       # 70 campaigns
    └── product_catalog.csv           # 37 products
```

## 🚀 Quick Start (3 Steps)

### 1. View the Data
```bash
# Already generated! Check the data folder:
ls -lh data/nourishbox/

# Preview a file:
head data/nourishbox/customers.csv
```

### 2. Run Sample Analysis
```bash
source venv/bin/activate
python example_analysis.py
```

### 3. Start Building Your Portfolio

**Choose your tool:**

#### Option A: Tableau / Power BI
1. Open Tableau/Power BI
2. Connect to CSV files in `data/nourishbox/`
3. Create dashboards (see ideas below)

#### Option B: SQL Database
1. Create database: `createdb nourishbox`
2. Load schema: `psql nourishbox < database_schema.sql`
3. Import CSVs using `COPY` commands or tool of choice
4. Run queries from `database_schema.sql`

#### Option C: Python/Jupyter
1. Create new notebook
2. Import pandas: `import pandas as pd`
3. Load data: `df = pd.read_csv('data/nourishbox/customers.csv')`
4. Start analyzing!

## 💡 Top 5 Dashboard Ideas

### 1. **Executive Dashboard** ⭐ (Start Here)
- MRR (Monthly Recurring Revenue) trend
- Active vs. Churned subscribers
- Key metrics: CAC, LTV, Churn Rate
- Revenue by subscription plan

**Skills demonstrated**: Business metrics, KPIs, time-series

### 2. **Customer Analytics Dashboard**
- Cohort retention curves
- Customer segmentation (RFM analysis)
- Acquisition channel performance
- Geographic distribution

**Skills demonstrated**: Cohort analysis, segmentation, attribution

### 3. **Churn Prediction & Analysis**
- Churn rate trends over time
- Churn reasons breakdown
- Customer risk scoring
- Retention offer effectiveness

**Skills demonstrated**: Predictive analytics, customer retention

### 4. **Product Performance Dashboard**
- Most popular meals by dietary preference
- Beauty product category trends
- Cross-sell analysis (Meal → Combo conversions)
- Product ratings vs. sales

**Skills demonstrated**: Product analytics, cross-selling

### 5. **Marketing ROI Dashboard**
- Campaign performance comparison
- Cost per acquisition by channel
- Conversion funnel analysis
- Attribution modeling

**Skills demonstrated**: Marketing analytics, ROI calculation

## 📊 Key Business Metrics (Already in the Data!)

| Metric | Value | Use Case |
|--------|-------|----------|
| **Total Revenue** | $2.2M | Revenue analysis |
| **Active Subscriptions** | 1,776 | Retention tracking |
| **Churn Rate** | 29% | Churn prediction |
| **Avg Order Value** | $68.41 | Customer value |
| **Avg Rating** | 4.14/5.0 | Quality metrics |
| **Customers** | 2,500 | Cohort analysis |
| **Orders** | 32,514 | Trend analysis |

## 🎨 Visualization Tips

### Must-Have Charts
1. **Line Chart**: MRR over time
2. **Cohort Heatmap**: Retention by signup month
3. **Funnel**: Marketing conversion funnel
4. **Bar Chart**: Churn reasons
5. **Scatter Plot**: Customer LTV vs. Age/Channel

### Color Scheme (Brand Consistent)
- Primary: `#4CAF50` (Green - health/meals)
- Secondary: `#E91E63` (Pink - beauty)
- Accent: `#FF9800` (Orange - combo)
- Neutral: `#607D8B` (Grey - data)

## 🔍 Sample Analysis Questions

**Answer these to impress interviewers:**

1. **What is the customer lifetime value by acquisition channel?**
   - Hint: Join customers, orders; group by channel

2. **Which subscription plan has the best retention?**
   - Hint: Calculate churn rate per plan type

3. **When do most customers churn?**
   - Hint: Analyze `subscription_length_days` in churn_events

4. **What's the ROI of our marketing campaigns?**
   - Hint: Revenue/Cost by campaign_type

5. **Can we predict which customers will churn?**
   - Hint: Build logistic regression model

## 💻 Sample SQL Queries

```sql
-- Top 10 customers by revenue
SELECT c.customer_id, c.first_name, c.last_name,
       SUM(o.order_total) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10;

-- Monthly churn rate
SELECT DATE_TRUNC('month', churn_date) as month,
       COUNT(*) as churns
FROM churn_events
GROUP BY month
ORDER BY month;

-- Revenue by plan type
SELECT s.plan_name,
       COUNT(DISTINCT o.order_id) as orders,
       SUM(o.order_total) as revenue
FROM subscriptions s
JOIN orders o ON s.subscription_id = o.subscription_id
GROUP BY s.plan_name
ORDER BY revenue DESC;
```

## 🎯 Portfolio Presentation Tips

### When showing to recruiters:

1. **Start with the business context**
   - "This is NourishBox, a subscription box service..."
   - Explain the business model briefly

2. **Show your process**
   - "I generated realistic synthetic data to avoid privacy issues"
   - "I created a star schema for optimal query performance"

3. **Highlight insights, not just charts**
   - ❌ "This shows revenue over time"
   - ✅ "Revenue grew 15% YoY, driven by Combo plan adoption"

4. **Demonstrate technical skills**
   - Mention: SQL joins, DAX calculations, Python pandas
   - Show: Data modeling, ETL process, dashboard design

5. **Prepare for questions**
   - "How would you reduce churn?" → Retention campaigns
   - "What's the next analysis?" → Predictive modeling

## 🔄 Customization Options

Want to make it unique? Modify these in `generate_nourishbox_data.py`:

```python
# Line 24-27
NUM_CUSTOMERS = 5000      # More customers
START_DATE = datetime(2020, 1, 1)  # Longer history
END_DATE = datetime(2025, 12, 31)  # Future data

# Line 29
SUBSCRIPTION_PLANS = {
    # Add your own plans!
}
```

Then regenerate:
```bash
python generate_nourishbox_data.py
```

## 📚 Learning Path

### Beginner → Intermediate → Advanced

**Week 1: Data Exploration**
- Load data into your BI tool
- Create basic charts (line, bar, pie)
- Calculate key metrics (revenue, churn rate)

**Week 2: Dashboard Building**
- Build Executive Dashboard
- Add filters and interactivity
- Design for mobile

**Week 3: Advanced Analytics**
- Cohort retention analysis
- RFM customer segmentation
- Marketing attribution

**Week 4: Predictive Modeling**
- Churn prediction (Python/R)
- Customer LTV forecasting
- A/B test simulation

## 🎓 Skills This Project Demonstrates

### Technical Skills
✅ SQL (joins, aggregations, window functions)
✅ Data visualization (dashboards, charts)
✅ Data modeling (star schema, relationships)
✅ ETL/ELT processes
✅ Python/R for analysis
✅ Statistics (cohort analysis, A/B testing)
✅ Machine learning (classification, regression)

### Business Skills
✅ Subscription business metrics (MRR, churn, LTV)
✅ Customer analytics
✅ Marketing ROI
✅ Product analytics
✅ Data storytelling
✅ Executive communication

## 🤝 Next Steps

1. **Build 1-2 dashboards** (use templates from README.md)
2. **Document your process** (screenshots, insights)
3. **Publish your work**:
   - Tableau Public
   - GitHub repository
   - Personal website/portfolio
4. **Write a case study**:
   - Problem → Analysis → Insights → Recommendations
5. **Practice presentation** (5-minute walkthrough)

## 📧 Portfolio Integration

### Resume Bullet Points (Examples)
- "Built interactive Tableau dashboard analyzing $2.2M in subscription revenue, identifying 15% revenue opportunity through churn reduction"
- "Performed cohort analysis on 2,500+ customers to calculate retention rates and customer lifetime value across 6 subscription tiers"
- "Developed predictive churn model using Python (scikit-learn) achieving 85% accuracy, enabling proactive retention campaigns"

### LinkedIn Project Description
```
NourishBox Business Intelligence Analysis

Analyzed a subscription box business combining healthy meals and beauty products:
• Designed and modeled relational database with 9 tables and 445K+ records
• Created executive dashboard tracking MRR, churn rate, and customer LTV
• Performed cohort retention analysis revealing 71% long-term retention
• Identified top 3 churn drivers, recommending targeted retention strategies
• Built predictive model to identify at-risk customers

Tools: [Your tools: Tableau/Power BI/SQL/Python]
Link: [Your portfolio link]
```

## ✨ Make It Yours!

**Personalization ideas:**
- Change business name/theme
- Add your own metrics
- Create custom visualizations
- Build unique ML models
- Write a blog post about insights

## 🎉 You're Ready!

You now have everything you need to build an impressive BI portfolio project. The data is realistic, comprehensive, and ready to analyze.

**Remember**: Employers care more about:
- Your analytical thinking
- How you communicate insights
- Your technical skills application
- Business impact of your work

...than about whether you used "real" data.

---

**Good luck with your portfolio!** 🚀

*Questions? Review the full [README.md](README.md) for detailed documentation.*
