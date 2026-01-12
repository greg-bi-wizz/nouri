# NourishBox - Business Intelligence Portfolio Project

A comprehensive synthetic dataset for a subscription box service combining healthy meals and beauty products. Perfect for demonstrating BI, analytics, and data science skills.

## 📊 Business Overview

**NourishBox** is a fictional subscription-based service delivering:
- **Healthy Meal Kits**: Pre-portioned ingredients with recipes (3-5 meals/week)
- **Beauty Products**: Curated skincare, makeup, and wellness items (4-6 items/month)
- **Combo Plans**: Combined meal and beauty subscriptions at discounted rates

### Business Model
- Monthly recurring subscriptions
- Six subscription tiers (Basic to Deluxe)
- Prices ranging from $35.99 to $119.99/month
- Customer preferences for dietary restrictions and beauty products
- Multi-channel acquisition strategy

## 📁 Dataset Overview

### Generated Data (2021-01-01 to 2025-12-31)

| Dataset | Records | Description |
|---------|---------|-------------|
| **customers.csv** | 4,015 | Customer demographics and acquisition data |
| **customer_preferences.csv** | 4,015 | Dietary restrictions, beauty preferences, allergies |
| **subscriptions.csv** | 4,301 | Subscription history including upgrades/cancellations |
| **subscription_monthly.csv** | 79,544 | Monthly subscription snapshots for MRR/NRR |
| **orders.csv** | 72,799 | Monthly box deliveries with seasonal patterns |
| **order_items.csv** | 1,011,604 | Individual products in each box (priced lines) |
| **churn_events.csv** | 1,912 | Cancellation details and reasons |
| **reviews.csv** | 27,389 | Customer ratings and feedback |
| **marketing_campaigns.csv** | 130 | Campaign performance metrics |
| **product_catalog.csv** | 37 | Available meal and beauty products |
| **plan_dim.csv** | 6 | Plan dimension (lookup) |
| **date_dim.csv** | 1,826 | Calendar dimension (2021-01-01 → 2025-12-31) |

### Key Business Metrics

- **Total Revenue**: $5.11M over 5 years (2021-2025)
- **Active Subscriptions**: 2,103 (52% of total customers)
- **Churn Rate**: 47.6% (influenced by New Year's resolution effect)
- **Average Order Value**: $70.24
- **Average Review Rating**: 4.15/5.0
- **Review Response Rate**: 40%
- **New Year Signups**: 1,424 customers (35% of total)

### 📊 Seasonality Features

This dataset includes **realistic seasonal business patterns**:

#### 1. **Customer Signup Seasonality**
- **January Peak**: 2.5x normal signup rate (New Year's resolutions)
- **February**: 2.0x normal rate
- **Summer Slowdown**: 0.5-0.6x rate (June-August)
- **Holiday Dip**: 0.6-0.7x rate (November-December)
- **Spring Boost**: 1.1-1.3x rate (March-May)

#### 2. **New Year's Resolution Effect**
- **35% of all customers** sign up in January-February
- **55% of New Year signups churn within 2-3 months**
- Dramatic retention cliff at month 3-4 for this cohort
- Perfect for analyzing "resolution abandonment" patterns

#### 3. **Seasonal Order Patterns**
- **Summer Pauses**: 12-15% skip rate (July peak)
- **Holiday Pauses**: 10-14% skip rate (December peak)
- **Normal Months**: 5-6% skip rate
- Seasonal variations create realistic order volume fluctuations throughout the year

## 🎯 BI Analysis Opportunities

This dataset is designed to showcase various BI and analytics skills:

### 1. **Customer Analytics**
- Customer lifetime value (CLV) analysis
- **Cohort analysis by registration month** (see [cohort_analysis.py](cohort_analysis.py))
- **New Year vs. regular cohort comparison**
- Acquisition channel effectiveness (CAC, ROI)
- Customer segmentation (RFM analysis, clustering)
- Demographic patterns in subscription preferences

### 2. **Churn & Retention Analysis**
- Churn prediction modeling
- Retention curve analysis with seasonal patterns
- **New Year's resolution churn analysis**
- Churn reason breakdown
- Early warning indicators (month 2-3 for Jan/Feb signups)
- Win-back campaign opportunities

### 3. **Product Performance**
- Meal vs. Beauty product popularity
- Cross-selling opportunities (meal-only → combo)
- Product preference by demographics
- Seasonal trends in product selection
- Dietary preference distribution

### 4. **Revenue Analysis**
- Monthly recurring revenue (MRR) trends
- Revenue by subscription tier
- Discount impact analysis
- Upsell/cross-sell revenue
- Customer payment behavior

### 5. **Marketing Analytics**
- Campaign ROI and conversion rates
- Channel attribution modeling
- Cost per acquisition by channel
- Referral program effectiveness
- Marketing spend optimization

### 6. **Seasonality Analysis**
- **Monthly signup patterns** (January spikes, summer dips)
- **Order skip rate by season** (vacation and holiday impact)
- **Revenue forecasting with seasonal decomposition**
- Cohort retention by signup month
- Marketing campaign timing optimization

### 7. **Operational Metrics**
- Delivery performance (on-time %)
- Order fulfillment issues
- **Seasonal order volume patterns** (12-15% summer pauses)
- Geographic distribution analysis

### 8. **Predictive Modeling**
- Churn prediction (classification)
- Customer lifetime value prediction (regression)
- Next-best subscription recommendation
- Optimal pricing analysis
- Demand forecasting

## 🚀 Getting Started

### Prerequisites
```bash
python 3.8+
pandas
numpy
faker
```

### Installation
```bash
# Clone or download this repository
cd my_portfolio_p4_aigen_data

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Data
```bash
# Run the data generator
python generate_nourishbox_data.py

# Data will be created in: data/nourishbox/
```

### Customization

You can modify the following parameters in [generate_nourishbox_data.py](generate_nourishbox_data.py):

```python
START_DATE = datetime(2021, 1, 1)    # Data start date
END_DATE = datetime(2025, 12, 31)    # Data end date
NUM_CUSTOMERS = 4015                 # Number of customers to generate
OUTPUT_DIR = 'data/nourishbox'       # Output directory
```

**Note**: The generator includes built-in seasonality patterns:
- **Customer signups** automatically reflect seasonal business cycles (January peaks, summer dips)
- **Order skip rates** vary by season (higher during summer vacations and holidays)
- **Churn patterns** include New Year's resolution effect (55% of Jan/Feb signups churn within 2-3 months)

## 📋 Data Dictionary

### customers.csv
| Column | Type | Description |
|--------|------|-------------|
| customer_id | string | Unique customer identifier (CUST000001) |
| first_name | string | Customer first name |
| last_name | string | Customer last name |
| email | string | Customer email address |
| phone | string | Customer phone number |
| registration_date | date | Account creation date |
| acquisition_channel | string | How customer found service (organic_search, paid_social, etc.) |
| age | integer | Customer age |
| gender | string | Gender (Female, Male, Non-binary, Prefer not to say) |
| zip_code | string | ZIP/postal code |
| city | string | City |
| state | string | State abbreviation |
| referred_by_customer_id | string | Referring customer ID (if applicable) |
| **is_new_year_signup** | **boolean** | **True if registered in January or February** |

### customer_preferences.csv
| Column | Type | Description |
|--------|------|-------------|
| customer_id | string | Unique customer identifier |
| dietary_preferences | string | Comma-separated dietary restrictions |
| beauty_preferences | string | Comma-separated beauty product preferences |
| skin_type | string | Skin type (normal, oily, dry, combination, sensitive) |
| allergies | string | Food allergies |
| preferred_meal_time | string | Lunch, dinner, or both |
| household_size | integer | Number of people in household |

**Dietary Preferences**: vegetarian, vegan, gluten_free, keto, paleo, dairy_free, low_carb, none

**Beauty Preferences**: anti_aging, acne_treatment, hydration, natural_organic, fragrance_free, vegan_beauty, luxury

### subscriptions.csv
| Column | Type | Description |
|--------|------|-------------|
| subscription_id | string | Unique subscription identifier |
| customer_id | string | Customer identifier |
| plan_type | string | Subscription plan key |
| plan_name | string | Human-readable plan name |
| monthly_price | float | Monthly subscription price |
| start_date | date | Subscription start date |
| end_date | date | Subscription end date (null if active) |
| status | string | active, cancelled, or upgraded |
| billing_cycle | string | Billing frequency (monthly) |
| auto_renew | boolean | Auto-renewal enabled |

### subscription_monthly.csv
| Column | Type | Description |
|--------|------|-------------|
| snapshot_id | string | Snapshot row identifier |
| subscription_id | string | Subscription identifier |
| customer_id | string | Customer identifier |
| plan_type | string | Plan key at snapshot |
| plan_name | string | Plan name at snapshot |
| month_start | date | First day of the snapshot month |
| status | string | Status at month start |
| mrr | float | Monthly recurring revenue for that subscription month |

**Plan Types**:
- `meal_basic`: 3 meals/week @ $49.99
- `meal_plus`: 5 meals/week @ $79.99
- `beauty_essentials`: 4 items/month @ $35.99
- `beauty_premium`: 6 items/month @ $59.99
- `combo_starter`: 3 meals + 3 beauty items @ $74.99
- `combo_deluxe`: 5 meals + 6 beauty items @ $119.99

### orders.csv
| Column | Type | Description |
|--------|------|-------------|
| order_id | string | Unique order identifier |
| subscription_id | string | Associated subscription |
| customer_id | string | Customer identifier |
| order_date | date | Order placement date |
| delivery_date | date | Actual/scheduled delivery date |
| order_total | float | Total order amount |
| delivery_status | string | delivered, delayed, cancelled, pending |
| shipping_cost | float | Shipping fee (free for orders >$50) |
| discount_applied | float | Discount amount |
| plan_type_at_order | string | Plan key at time of order |
| plan_price_at_order | float | List price of plan at time of order |
| campaign_id | string | Attributed campaign (nullable) |
| order_date_key | integer | Date key linking to date_dim |
| year_month | string | Order year-month (YYYY-MM) |

### order_items.csv
| Column | Type | Description |
|--------|------|-------------|
| item_id | string | Unique item identifier |
| order_id | string | Associated order |
| product_type | string | meal or beauty |
| product_name | string | Product name |
| product_category | string | Product subcategory |
| quantity | integer | Quantity (typically 1) |
| unit_cost | float | Cost per unit to company |
| line_price | float | Billed price for the line |
| line_discount | float | Allocated discount amount for the line |
| calories | integer | Calories (meals only) |
| retail_value | float | Retail value (beauty products only) |
| tags | string | Product tags/attributes |

### churn_events.csv
| Column | Type | Description |
|--------|------|-------------|
| churn_id | string | Unique churn event identifier |
| subscription_id | string | Cancelled subscription |
| customer_id | string | Customer identifier |
| churn_date | date | Cancellation date |
| subscription_length_days | integer | Days customer was subscribed |
| churn_reason | string | Primary reason for cancellation |
| attempted_retention | boolean | Retention offer made |
| retention_offer_accepted | boolean | Whether retention succeeded |
| feedback_provided | boolean | Customer provided feedback |
| feedback_text | string | Open-text feedback |

**Churn Reasons**: too_expensive, moving, product_quality, variety_lacking, dietary_needs_changed, prefer_competitor, financial_reasons, delivery_issues, too_much_food, lifestyle_change, other

### reviews.csv
| Column | Type | Description |
|--------|------|-------------|
| review_id | string | Unique review identifier |
| order_id | string | Reviewed order |
| customer_id | string | Reviewer |
| subscription_id | string | Active subscription |
| review_date | date | Review submission date |
| rating | integer | Overall rating (1-5 stars) |
| review_title | string | Review headline |
| review_text | string | Detailed review text |
| would_recommend | boolean | Would recommend to others |
| meal_quality_rating | integer | Meal quality (1-5) |
| beauty_quality_rating | integer | Beauty product quality (1-5) |
| delivery_rating | integer | Delivery experience (1-5) |
| value_rating | integer | Value for money (1-5) |

### marketing_campaigns.csv
| Column | Type | Description |
|--------|------|-------------|
| campaign_id | string | Unique campaign identifier |
| campaign_name | string | Campaign name |
| campaign_type | string | email, social_media, influencer, paid_ads, referral_bonus, partnership |
| start_date | date | Campaign start |
| end_date | date | Campaign end |
| budget | float | Campaign budget |
| target_audience | string | new_customers, existing_customers, churned_customers, all |
| offer_type | string | discount_percent, discount_fixed, free_trial, free_gift, none |
| offer_value | integer | Discount percentage or fixed amount |
| impressions | integer | Total impressions |
| clicks | integer | Total clicks |
| conversions | integer | Total conversions |
| ctr | float | Click-through rate (%) |
| conversion_rate | float | Conversion rate (%) |
| cost_per_acquisition | float | Cost per converted customer |

### product_catalog.csv
| Column | Type | Description |
|--------|------|-------------|
| product_id | string | Unique product identifier |
| product_type | string | meal or beauty |
| product_name | string | Product name |
| category | string | Product category |
| cost_to_company | float | Company's cost |
| calories | integer | Calories (meals only) |
| retail_value | float | Retail value (beauty only) |
| tags | string | Product attributes |
| active | boolean | Currently available |

### plan_dim.csv
| Column | Type | Description |
|--------|------|-------------|
| plan_key | string | Plan key (matches plan_type) |
| plan_name | string | Human-readable plan name |
| category | string | meals, beauty, combo |
| monthly_price | float | Standard monthly list price |
| meals_per_week | integer | Meals per week (meal/combo plans) |
| items_per_month | integer | Beauty items per month (beauty/combo plans) |

### date_dim.csv
| Column | Type | Description |
|--------|------|-------------|
| date_key | integer | Surrogate key YYYYMMDD |
| calendar_date | date | Calendar date |
| year | integer | Calendar year |
| quarter | integer | Calendar quarter |
| month | integer | Month number |
| day | integer | Day of month |
| day_of_week | integer | ISO weekday (Mon=1) |
| month_name | string | Month name |
| year_month | string | YYYY-MM |
| is_weekend | boolean | Weekend flag |
| season | string | winter/spring/summer/fall |

## 🎨 Visualization Ideas

### Dashboards to Build

1. **Executive Dashboard**
   - MRR trend and forecast
   - Active subscribers vs. churned
   - Revenue by plan type
   - Key metrics (CLV, CAC, churn rate)

2. **Customer Analytics Dashboard**
   - Cohort retention curves
   - Customer segmentation matrix
   - Acquisition channel funnel
   - Geographic heat map

3. **Product Performance Dashboard**
   - Most popular meals by dietary preference
   - Beauty product category breakdown
   - Cross-sell success (meal → combo conversion)
   - Product ratings distribution

4. **Churn Analysis Dashboard**
   - Churn reasons breakdown
   - Churn rate by cohort
   - At-risk customer segments
   - Retention offer effectiveness

5. **Marketing ROI Dashboard**
   - Campaign performance comparison
   - Channel attribution
   - Cost per acquisition trends
   - Conversion funnel by campaign

## ☁️ Cloud Deployment Options

Deploy your data to cloud platforms for professional portfolio projects:

### **Option 1: Databricks (Enterprise Big Data)**
- **Free**: Community Edition available
- **Best for**: Big data analytics, Apache Spark, ML pipelines
- **Guide**: [DATABRICKS_SETUP.md](DATABRICKS_SETUP.md)
- **Setup**: `python src/sync_to_databricks.py --clear`
- **Portfolio Impact**: Delta Lake, Spark SQL, enterprise data engineering

### **Option 2: Supabase (PostgreSQL Cloud)**
- **Free**: 500 MB database
- **Best for**: Power BI connection, REST API access
- **Guide**: [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
- **Setup**: `python src/sync_to_supabase.py --clear`
- **Portfolio Impact**: Cloud database, real-time BI dashboards

### **Other Options**
- **Google BigQuery**: Large-scale analytics (10 GB free)
- **Kaggle Datasets**: Community visibility and sharing
- **GitHub**: Version control and code showcase

See full comparison and setup guides: [CLOUD_SETUP_GUIDE.md](CLOUD_SETUP_GUIDE.md)

---

## 🛠️ Tools & Technologies

This dataset can be used with:

- **BI Tools**: Tableau, Power BI, Looker, Metabase, Qlik
- **Cloud Platforms**: Databricks, Supabase, BigQuery, Snowflake
- **SQL Databases**: PostgreSQL, MySQL, SQLite
- **Python**: pandas, matplotlib, seaborn, plotly, scikit-learn
- **R**: tidyverse, ggplot2, caret, shiny
- **Spreadsheets**: Excel, Google Sheets (sample data)

## 📈 Sample Analysis Questions

### Business Questions to Answer

1. What is the customer lifetime value by acquisition channel?
2. Which subscription plan has the highest retention rate?
3. **What are the retention rates for New Year signups vs. other months?**
4. **How does signup month affect 90-day retention rates?**
5. What are the top 3 reasons customers churn, and when?
6. How does dietary preference correlate with churn risk?
7. What is the ROI of each marketing campaign type?
8. Which products drive the highest customer satisfaction?
9. **What seasonal patterns exist in order skip rates (vacations/holidays)?**
10. **Should marketing spend increase in January despite higher churn?**
11. What is the typical upgrade path from basic to premium plans?
12. How does household size impact subscription plan choice?
13. **At what months should retention campaigns target January signups?**
14. What is the optimal discount level to maximize conversions without hurting margins?
15. **How does cumulative LTV differ between New Year and regular cohorts?**

## 📝 Project Ideas

### Beginner
- Create a basic dashboard showing revenue trends
- Calculate average customer lifetime
- Visualize churn reasons as a pie chart
- Build a customer demographics report
- **Plot monthly signup trends with seasonal patterns**

### Intermediate
- **Cohort analysis with retention heatmaps** (see [cohort_analysis.py](cohort_analysis.py))
- **New Year vs. regular cohort comparison**
- RFM segmentation model
- A/B test simulation for pricing strategies
- Predictive churn model (logistic regression)
- **Seasonal order skip rate analysis**

### Advanced
- **Customer lifetime value prediction by signup month** (ML)
- Recommendation engine for subscription upgrades
- Multi-channel attribution modeling
- **Demand forecasting with seasonal decomposition**
- Causal impact analysis of marketing campaigns
- **Retention intervention timing optimization for January cohorts**

## 🔄 Data Relationships

```
customers (1) ──→ (n) subscriptions
    │                    │
    │                    │
    └──→ (1:1) customer_preferences
                         │
                         ↓
               subscriptions (1) ──→ (n) orders
                         │                │
                         │                │
                         ↓                ↓
                  churn_events      order_items
                                          │
                                          ↓
                                   product_catalog

orders (1) ──→ (n) reviews
```

## 🔬 Analysis Scripts Included

### Cohort Analysis ([cohort_analysis.py](cohort_analysis.py))

Comprehensive cohort retention analysis with visualizations:

**Features:**
- **Retention Heatmap**: Month-by-month retention rates for each signup cohort
- **New Year vs. Others Comparison**: Dramatic difference in retention curves
- **Average Retention Trends**: Overall retention patterns across all cohorts
- **Cumulative LTV Heatmap**: Lifetime value progression by cohort
- **LTV Curve**: Average customer value over 12 months

**Key Insights Generated:**
- Month 1-12 retention rates
- 3-month retention comparison (New Year: ~67%, Others: ~81%)
- Cumulative LTV at 3, 6, and 12 months
- Best and worst performing cohorts
- Critical drop-off points

**Usage:**
```bash
python cohort_analysis.py
# Generates: data/nourishbox/cohort_analysis.png
```

**Example Output:**
```
1. RETENTION RATES:
   • Month 1:  95.5% of customers place a 2nd order
   • Month 3:  74.2% retention (critical milestone)
   • Month 6:  64.8% retention
   • Month 12: 52.1% retention

2. NEW YEAR COHORT PERFORMANCE:
   • 3-month retention (New Year): 67.2%
   • 3-month retention (Others):   80.8%
   • Difference: -13.5% (New Year signups drop off faster)

3. CUSTOMER LIFETIME VALUE:
   • 3-month LTV:  $208.50
   • 6-month LTV:  $356.25
   • 12-month LTV: $625.75
```

### Seasonality Analysis ([analyze_seasonality.py](analyze_seasonality.py))

Analyzes seasonal patterns in signups, orders, and revenue:

**Features:**
- Monthly signup volume with deviations from average
- New Year's resolution churn analysis
- Order volume by season
- Revenue seasonality patterns
- Churn timing analysis

**Usage:**
```bash
python analyze_seasonality.py
# Generates: data/nourishbox/seasonality_analysis.png
```

## 📚 Learning Resources

To maximize learning from this dataset:

1. **SQL Practice**: Write queries to answer the sample questions
2. **Data Modeling**: Create an ERD (Entity Relationship Diagram)
3. **ETL**: Build pipelines to load data into your BI tool
4. **Visualization**: Follow dashboard best practices
5. **Statistics**: Calculate significance of trends and differences
6. **Machine Learning**: Build and evaluate predictive models

## 🤝 Contributing

This is a portfolio project. Feel free to:
- Modify the data generation parameters
- Add new product categories
- Create additional tables (e.g., customer support tickets)
- Extend the date range
- Share your analysis and dashboards

## 📄 License

This synthetic dataset is generated for educational and portfolio purposes. Feel free to use it in your projects, portfolios, and learning exercises.

## ⚠️ Disclaimer

This is **synthetic data** generated using the Faker library and custom algorithms. All names, addresses, emails, and phone numbers are fictional. Any resemblance to real persons or businesses is purely coincidental.

---

**Created for Business Intelligence Portfolio Projects**

### ✨ What Makes This Dataset Special

Unlike typical synthetic datasets, NourishBox includes:
- **Realistic seasonality** with January signup spikes (2.5x normal rate) and summer/holiday dips (0.5-0.6x rate)
- **New Year's resolution effect** showing 55% early churn for Jan/Feb signups (35% of all customers)
- **Seasonal order patterns** with vacation and holiday pauses (12-15% summer skip rate, 10-14% holiday skip rate)
- **5 years of data** (2021-2025) with over 1 million order line items
- **Complete cohort analysis tools** ready to showcase retention analytics
- **Built-in churn patterns** that distinguish between New Year cohorts and regular cohorts

Perfect for demonstrating advanced BI skills like cohort analysis, seasonal forecasting, and customer behavior modeling.

*Last Updated: January 2025*
