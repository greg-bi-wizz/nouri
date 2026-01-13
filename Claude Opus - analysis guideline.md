
User: connect to powerbi desktop using mcp and analyze the model and prepare analytical description of the model

GitHub Copilot: Enable Claude Opus 4.5 for all clients
[object Object]

User: @agent Enable: "Enable Claude Opus 4.5 for all clients"

GitHub Copilot: I'll help you connect to Power BI Desktop and analyze the model. Let me first find the available local instances. 

Ran `connection_operations` 
Completed with input: {
  "request": {
    "operation": "ListLocalInstances"
  }
}

Found a Power BI Desktop instance. Let me connect to it and then analyze the model structure. 

Ran `connection_operations` 
Completed with input: {
  "request": {
    "operation": "Connect",
    "connectionString": "Data Source=localhost:51361;Application Name=MCP-PBIModeling"
  }
}

Connected successfully. Now let me gather comprehensive information about the model by fetching tables, measures, relationships, and model details. 

Ran `model_operations` 
Completed with input: {
  "request": {
    "operation": "Get"
  }
}

Ran `table_operations` 
Completed with input: {
  "request": {
    "operation": "List"
  }
}

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "List"
  }
}

Ran `relationship_operations` 
Completed with input: {
  "request": {
    "operation": "List"
  }
}

Got basic model info and table list. Let me retry fetching the measures and relationships, and also get column details for key tables. 

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "List"
  }
}

Ran `relationship_operations` 
Completed with input: {
  "request": {
    "operation": "List"
  }
}

Now let me get the measure expressions and details about the key tables. 

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "Get",
    "measureName": "Total Orders"
  }
}

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "Get",
    "measureName": "Total Revenue"
  }
}

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "Get",
    "measureName": "AOV"
  }
}

Ran `measure_operations` 
Completed with input: {
  "request": {
    "operation": "Get",
    "measureName": "Active Subs"
  }
}

Excellent! Now let me get column details for key tables to understand the data structure better. 

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "dim_customers"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "orders"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "subscriptions"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "dim_plan"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "churn_events"
  }
}

Let me get details on the remaining important tables. 

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "order_items"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "dim_product_catalog"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "reviews"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "marketing_campaigns"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "subscription_monthly"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "dim_date"
  }
}

Ran `column_operations` 
Completed with input: {
  "request": {
    "operation": "List",
    "tableName": "dim_customer_preferences"
  }
}

Now I have comprehensive information about the model. Let me provide you with an analytical description.

---

## 📊 Nurish Box - Semantic Model Analysis

### **Model Overview**

| Property | Value |
|----------|-------|
| **Model Name** | nurish_box2 |
| **Data Mode** | Import |
| **Culture** | en-US |
| **Tables** | 13 |
| **Relationships** | 15 |
| **Measures** | 4 |

This is a **subscription-based e-commerce/wellness box business model** that combines **meal delivery** and **beauty products**. The data model supports analysis of customer subscriptions, orders, churn, marketing effectiveness, and customer feedback.

---

### **📁 Table Architecture**

#### **Dimension Tables (7)**

| Table | Columns | Description |
|-------|---------|-------------|
| `dim_customers` | 14 | Customer demographics, registration, acquisition channel, geographic data |
| `dim_customer_preferences` | 7 | Dietary preferences, beauty preferences, skin type, allergies |
| `dim_plan` | 6 | Subscription plan catalog with pricing and meal/item counts |
| `dim_product_catalog` | 9 | Product master data with costs, categories, and nutritional info |
| `dim_date` | 11 | Standard date dimension with year, month, quarter, weekday, season |
| `marketing_campaigns` | 15 | Campaign details with budget, performance metrics (CTR, conversions) |
| `_Base_Measures` | 1 | Measures-only table for storing DAX calculations |

#### **Fact Tables (6)**

| Table | Columns | Description |
|-------|---------|-------------|
| `orders` | 15 | Order transactions with totals, delivery status, discounts, campaign attribution |
| `order_items` | 13 | Line-item detail with products, quantities, pricing |
| `subscriptions` | 10 | Customer subscriptions with plan, status, billing cycle, auto-renew |
| `subscription_monthly` | 8 | Monthly snapshots for MRR (Monthly Recurring Revenue) tracking |
| `churn_events` | 10 | Churn records with reasons, retention attempts, feedback |
| `reviews` | 13 | Customer feedback with multi-dimensional ratings |

---

### **🔗 Relationship Structure**

The model uses a **star schema** with hybrid patterns:

```
                    ┌──────────────────┐
                    │  dim_customers   │
                    └────────┬─────────┘
                             │ (1:1)
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
    ▼                        ▼                        ▼
┌───────────┐     ┌─────────────────────┐     ┌──────────────┐
│ churn_    │     │dim_customer_        │     │ subscriptions│
│ events    │     │preferences          │     │              │
└───────────┘     └─────────────────────┘     └──────┬───────┘
                                                     │ (1:*)
                    ┌────────────────────────────────┼────────┐
                    │                  │             │        │
                    ▼                  ▼             ▼        ▼
             ┌──────────┐    ┌────────────────┐  ┌────────┐ ┌─────────────────┐
             │ orders   │    │subscription_   │  │reviews │ │ dim_plan        │
             └────┬─────┘    │monthly         │  └────────┘ └─────────────────┘
                  │          └────────────────┘
                  ▼
        ┌─────────────────┐
        │marketing_       │
        │campaigns        │
        └─────────────────┘
```

**Key Relationship Details:**
- **Subscriptions** acts as the central fact table linking customers to orders, reviews, churn events, and monthly snapshots
- **Bi-directional filtering** enabled for customer preferences and churn analysis
- Some relationships are **inactive** (shown with `isActive: false`) to avoid circular references - these can be activated using USERELATIONSHIP() in DAX

---

### **📐 Measures Analysis**

| Measure | DAX Expression | Format | Purpose |
|---------|----------------|--------|---------|
| **Total Orders** | `COUNTROWS(orders)` | Number | Transaction count KPI |
| **Total Revenue** | `SUM(orders[order_total])` | Currency ($) | Revenue KPI |
| **AOV** | `DIVIDE([Total Revenue],[Total Orders])` | Currency ($) | Average Order Value metric |
| **Active Subs** | `CALCULATE(DISTINCTCOUNT(subscriptions[subscription_id]), subscriptions[status]="active")` | Number | Active subscription count |

---

### **💡 Analytical Capabilities**

This model enables the following types of analysis:

1. **Subscription Analytics**
   - Active/inactive subscription tracking
   - Monthly Recurring Revenue (MRR) trends via `subscription_monthly`
   - Plan-level performance comparison

2. **Customer Lifecycle Analysis**
   - Acquisition channel effectiveness
   - Customer demographics and preferences correlation
   - Churn analysis with reason tracking

3. **Revenue & Order Analytics**
   - Revenue trends and order volumes
   - Average Order Value (AOV) tracking
   - Discount impact analysis
   - Shipping cost analysis

4. **Marketing Attribution**
   - Campaign performance (CTR, conversion rate, CPA)
   - Order-to-campaign attribution via `campaign_id`
   - Budget efficiency analysis

5. **Product Performance**
   - Product-level sales analysis via `order_items`
   - Category analysis (meals vs. beauty products)
   - Margin analysis (cost vs. retail value)

6. **Customer Satisfaction**
   - Multi-dimensional ratings (meal quality, beauty quality, delivery)
   - Recommendation likelihood tracking
   - Review sentiment analysis capability

---

### **⚠️ Model Observations & Recommendations**

| Area                       | Observation                                      | Recommendation                                          |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------------- |
| **Missing Relationships**  | `order_items` ↔ `dim_product_catalog` not linked | Create relationship on `product_id`                     |
| **Missing Relationships**  | `dim_date` has no active relationships           | Connect to orders/subscriptions date columns            |
| **Inactive Relationships** | 6 relationships marked inactive                  | Document when to use USERELATIONSHIP()                  |
| **Limited Measures**       | Only 4 measures defined                          | Add MRR, Churn Rate, Retention Rate, ARPU measures      |
| **No Calculated Columns**  | Basic structure only                             | Consider adding Customer Lifetime Value, cohort columns |
| **No Time Intelligence**   | Annotation shows `TimeIntelligenceEnabled=0`     | Enable and add YoY, MoM calculations                    |

---

### **📈 Suggested Additional Measures**

```dax
// Monthly Recurring Revenue
MRR = SUM(subscription_monthly[mrr])

// Churn Rate
Churn Rate = DIVIDE(COUNTROWS(churn_events), [Active Subs] + COUNTROWS(churn_events))

// Average Rating
Avg Rating = AVERAGE(reviews[rating])

// Campaign ROI
Campaign ROI = DIVIDE([Total Revenue], SUM(marketing_campaigns[budget]))
```

---

This model is well-structured for a **subscription box business** with strong foundations for customer, order, and subscription analytics. The combination of meal and beauty products suggests a **holistic wellness subscription service** (hence "Nurish Box"). The model would benefit from additional calculated measures and time intelligence capabilities to unlock its full analytical potential.

User: Suggest additional calculated measures and time intelligence capabilities. Explain each suggested feature and also provide information how to visualize it in power bi

GitHub Copilot: ## 📊 Recommended Measures & Time Intelligence for Nurish Box Model

Based on the model analysis, here are comprehensive measure recommendations organized by analytical domain:

---

## 1️⃣ **Revenue & Order Metrics**

### **Total Items Sold**
```dax
Total Items Sold = SUM(order_items[quantity])
```
**Purpose:** Tracks product volume independent of revenue
**Visualization:** 
- **Card** for KPI display
- **Clustered Column Chart** with `dim_product_catalog[category]` on axis for product mix analysis

---

### **Gross Margin**
```dax
Gross Margin = 
SUMX(
    order_items,
    order_items[line_price] - (order_items[quantity] * RELATED(dim_product_catalog[cost_to_company]))
)
```
**Purpose:** Calculates profit after product costs
**Visualization:**
- **Gauge** comparing to target margin
- **Line Chart** trending over `dim_date[year_month]`

---

### **Gross Margin %**
```dax
Gross Margin % = DIVIDE([Gross Margin], [Total Revenue], 0)
```
**Purpose:** Profitability percentage for benchmarking
**Visualization:**
- **KPI Card** with conditional formatting (green >30%, yellow 20-30%, red <20%)
- **Matrix** by product category to identify high/low margin products

---

### **Discount Rate**
```dax
Discount Rate = 
DIVIDE(
    SUM(orders[discount_applied]),
    SUM(orders[order_total]) + SUM(orders[discount_applied]),
    0
)
```
**Purpose:** Monitors discounting levels
**Visualization:**
- **Line Chart** with `dim_date[year_month]` to track discount trends
- **Scatter Plot** with AOV on Y-axis to analyze discount impact on basket size

---

### **Shipping Revenue Ratio**
```dax
Shipping Revenue Ratio = DIVIDE(SUM(orders[shipping_cost]), [Total Revenue], 0)
```
**Purpose:** Tracks shipping as percentage of revenue
**Visualization:**
- **Area Chart** over time
- **Card** with conditional formatting

---

## 2️⃣ **Subscription & MRR Metrics**

### **Monthly Recurring Revenue (MRR)**
```dax
MRR = SUM(subscription_monthly[mrr])
```
**Purpose:** Core SaaS/subscription metric
**Visualization:**
- **Line Chart** trending over months
- **Card** showing current month value

---

### **Total Subscriptions**
```dax
Total Subscriptions = DISTINCTCOUNT(subscriptions[subscription_id])
```
**Purpose:** Total subscription count regardless of status
**Visualization:**
- **Donut Chart** broken down by `subscriptions[status]`

---

### **Active Subscription Rate**
```dax
Active Subscription Rate = DIVIDE([Active Subs], [Total Subscriptions], 0)
```
**Purpose:** Health indicator of subscription base
**Visualization:**
- **Gauge** with target at 80%+
- **Card** with percentage formatting

---

### **Average Revenue Per User (ARPU)**
```dax
ARPU = DIVIDE([Total Revenue], DISTINCTCOUNT(orders[customer_id]), 0)
```
**Purpose:** Revenue efficiency per customer
**Visualization:**
- **Line Chart** trending over time
- **Bar Chart** segmented by `dim_plan[plan_name]`

---

### **Average Subscription Length (Days)**
```dax
Avg Subscription Length = 
AVERAGEX(
    FILTER(subscriptions, subscriptions[status] = "cancelled" || subscriptions[status] = "expired"),
    DATEDIFF(subscriptions[start_date], subscriptions[end_date], DAY)
)
```
**Purpose:** Customer retention duration
**Visualization:**
- **Card** showing average days
- **Histogram** (using binned calculated column) for distribution

---

## 3️⃣ **Churn & Retention Metrics**

### **Churned Customers**
```dax
Churned Customers = DISTINCTCOUNT(churn_events[customer_id])
```
**Purpose:** Count of customers who left
**Visualization:**
- **Card** for KPI
- **Waterfall Chart** showing subscriber gains/losses

---

### **Churn Rate**
```dax
Churn Rate = 
DIVIDE(
    [Churned Customers],
    [Churned Customers] + DISTINCTCOUNT(subscriptions[customer_id]),
    0
)
```
**Purpose:** Percentage of customer attrition
**Visualization:**
- **KPI Card** with red conditional formatting when >5%
- **Line Chart** over time with target line

---

### **Retention Rate**
```dax
Retention Rate = 1 - [Churn Rate]
```
**Purpose:** Inverse of churn - percentage retained
**Visualization:**
- **Gauge** with green zone at 95%+
- **Card** prominently displayed

---

### **Retention Offer Success Rate**
```dax
Retention Offer Success Rate = 
DIVIDE(
    COUNTROWS(FILTER(churn_events, churn_events[retention_offer_accepted] = TRUE)),
    COUNTROWS(FILTER(churn_events, churn_events[attempted_retention] = TRUE)),
    0
)
```
**Purpose:** Effectiveness of retention campaigns
**Visualization:**
- **Card** with percentage
- **Funnel Chart**: Churn Events → Retention Attempted → Offer Accepted

---

### **Churn by Reason**
```dax
Churn by Reason % = 
DIVIDE(
    COUNTROWS(churn_events),
    CALCULATE(COUNTROWS(churn_events), REMOVEFILTERS(churn_events[churn_reason])),
    0
)
```
**Purpose:** Distribution of churn reasons
**Visualization:**
- **Pie Chart** or **Treemap** by `churn_events[churn_reason]`
- **Bar Chart** showing top reasons

---

## 4️⃣ **Customer Satisfaction Metrics**

### **Average Rating**
```dax
Avg Rating = AVERAGE(reviews[rating])
```
**Purpose:** Overall customer satisfaction score
**Visualization:**
- **Card** with star icon
- **Line Chart** trending over time

---

### **NPS Proxy (Would Recommend %)**
```dax
Would Recommend % = 
DIVIDE(
    COUNTROWS(FILTER(reviews, reviews[would_recommend] = TRUE)),
    COUNTROWS(reviews),
    0
)
```
**Purpose:** Proxy for Net Promoter Score
**Visualization:**
- **Gauge** with target at 80%
- **Card** with thumbs up icon

---

### **Avg Meal Quality Rating**
```dax
Avg Meal Quality = AVERAGE(reviews[meal_quality_rating])
```
**Purpose:** Product-specific quality tracking
**Visualization:**
- **Multi-row Card** showing all quality dimensions together
- **Radar Chart** comparing meal, beauty, delivery ratings

---

### **Avg Delivery Rating**
```dax
Avg Delivery Rating = AVERAGE(reviews[delivery_rating])
```
**Purpose:** Logistics performance tracking
**Visualization:**
- **Card** with conditional formatting
- **Map** visualization by delivery zip code

---

### **Review Response Rate**
```dax
Review Response Rate = 
DIVIDE(
    COUNTROWS(reviews),
    [Total Orders],
    0
)
```
**Purpose:** Engagement - how many orders get reviewed
**Visualization:**
- **Card** showing percentage
- **Line Chart** over time

---

## 5️⃣ **Marketing & Acquisition Metrics**

### **Campaign ROI**
```dax
Campaign ROI = 
DIVIDE(
    [Total Revenue] - SUM(marketing_campaigns[budget]),
    SUM(marketing_campaigns[budget]),
    0
)
```
**Purpose:** Return on marketing investment
**Visualization:**
- **Bar Chart** by `marketing_campaigns[campaign_name]`
- **Scatter Plot** with budget on X, revenue on Y

---

### **Cost Per Acquisition (Actual)**
```dax
Actual CPA = 
DIVIDE(
    SUM(marketing_campaigns[budget]),
    DISTINCTCOUNT(orders[customer_id]),
    0
)
```
**Purpose:** Real cost to acquire a customer
**Visualization:**
- **Card** compared to target CPA
- **Line Chart** trending over campaigns

---

### **Conversion Rate**
```dax
Overall Conversion Rate = 
DIVIDE(
    SUM(marketing_campaigns[conversions]),
    SUM(marketing_campaigns[clicks]),
    0
)
```
**Purpose:** Marketing funnel efficiency
**Visualization:**
- **Funnel Chart**: Impressions → Clicks → Conversions
- **Bar Chart** by campaign type

---

### **Customer Acquisition by Channel**
```dax
Customers by Channel = DISTINCTCOUNT(dim_customers[customer_id])
```
**Purpose:** Used with acquisition_channel slicer
**Visualization:**
- **Donut Chart** by `dim_customers[acquisition_channel]`
- **Stacked Bar Chart** over time

---

## 6️⃣ **Time Intelligence Measures** ⏰

> **Prerequisites:** Ensure `dim_date` table is marked as a **Date Table** in Power BI (Model view → right-click table → Mark as date table)

### **Revenue YTD (Year-to-Date)**
```dax
Revenue YTD = 
TOTALYTD([Total Revenue], dim_date[date])
```
**Purpose:** Cumulative revenue for the year
**Visualization:**
- **Area Chart** showing cumulative growth through year
- **Card** for executive dashboard

---

### **Revenue MTD (Month-to-Date)**
```dax
Revenue MTD = 
TOTALMTD([Total Revenue], dim_date[date])
```
**Purpose:** Cumulative revenue for current month
**Visualization:**
- **Card** for daily tracking
- **Line Chart** comparing current vs previous month MTD

---

### **Revenue QTD (Quarter-to-Date)**
```dax
Revenue QTD = 
TOTALQTD([Total Revenue], dim_date[date])
```
**Purpose:** Quarterly performance tracking
**Visualization:**
- **Card** in quarterly reports
- **Clustered Column Chart** comparing quarters

---

### **Revenue Previous Month**
```dax
Revenue PM = 
CALCULATE(
    [Total Revenue],
    DATEADD(dim_date[date], -1, MONTH)
)
```
**Purpose:** Last month comparison baseline
**Visualization:**
- **Card** with variance indicator
- **Line Chart** showing current vs previous

---

### **Revenue MoM Change (Month-over-Month)**
```dax
Revenue MoM Change = [Total Revenue] - [Revenue PM]
```
**Purpose:** Absolute monthly change
**Visualization:**
- **Card** with up/down arrows
- **Waterfall Chart** showing monthly contributions

---

### **Revenue MoM % Change**
```dax
Revenue MoM % = DIVIDE([Revenue MoM Change], [Revenue PM], 0)
```
**Purpose:** Percentage monthly growth
**Visualization:**
- **KPI visual** with trend indicator
- **Line Chart** showing growth rate over time

---

### **Revenue Previous Year**
```dax
Revenue PY = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(dim_date[date])
)
```
**Purpose:** Year-over-year comparison
**Visualization:**
- **Clustered Column Chart** (current year vs last year by month)
- **Line Chart** with two series

---

### **Revenue YoY Change (Year-over-Year)**
```dax
Revenue YoY Change = [Total Revenue] - [Revenue PY]
```
**Purpose:** Absolute yearly variance
**Visualization:**
- **Card** with conditional formatting
- **Variance Chart**

---

### **Revenue YoY % Change**
```dax
Revenue YoY % = DIVIDE([Revenue YoY Change], [Revenue PY], 0)
```
**Purpose:** Percentage yearly growth
**Visualization:**
- **KPI visual** comparing to target growth
- **Heat Map Matrix** by month showing YoY performance

---

### **Orders YTD**
```dax
Orders YTD = TOTALYTD([Total Orders], dim_date[date])
```
**Purpose:** Cumulative order count
**Visualization:**
- **Area Chart** with cumulative orders
- **Card** for KPI

---

### **Orders Previous Month**
```dax
Orders PM = 
CALCULATE(
    [Total Orders],
    DATEADD(dim_date[date], -1, MONTH)
)
```
**Purpose:** Order volume comparison
**Visualization:**
- **Line Chart** current vs previous
- **Card** with trend

---

### **MRR Previous Month**
```dax
MRR PM = 
CALCULATE(
    [MRR],
    DATEADD(dim_date[date], -1, MONTH)
)
```
**Purpose:** Subscription revenue comparison
**Visualization:**
- **Line Chart** MRR trend
- **Card** with growth indicator

---

### **MRR Growth Rate**
```dax
MRR Growth Rate = DIVIDE([MRR] - [MRR PM], [MRR PM], 0)
```
**Purpose:** Monthly subscription growth
**Visualization:**
- **KPI Card** with target
- **Line Chart** showing growth stability

---

### **Rolling 3-Month Average Revenue**
```dax
Revenue 3M Avg = 
AVERAGEX(
    DATESINPERIOD(dim_date[date], MAX(dim_date[date]), -3, MONTH),
    [Total Revenue]
)
```
**Purpose:** Smooths volatility for trend analysis
**Visualization:**
- **Line Chart** overlaid on actual revenue
- Shows underlying trend

---

### **Rolling 12-Month Revenue**
```dax
Revenue TTM = 
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(dim_date[date], MAX(dim_date[date]), -12, MONTH)
)
```
**Purpose:** Trailing twelve months (TTM) - annualized view
**Visualization:**
- **Card** for annual run rate
- **Line Chart** showing TTM trend

---

### **New Customers This Month**
```dax
New Customers MTD = 
CALCULATE(
    DISTINCTCOUNT(dim_customers[customer_id]),
    DATESMTD(dim_date[date]),
    dim_customers[registration_date] >= MIN(dim_date[date])
)
```
**Purpose:** Customer acquisition velocity
**Visualization:**
- **Card** for current performance
- **Line Chart** month over month

---

## 📋 Visualization Dashboard Recommendations

### **Executive Dashboard**
| Visual | Measures | Purpose |
|--------|----------|---------|
| Card Row | Total Revenue, Total Orders, Active Subs, AOV | Top-line KPIs |
| KPI Cards | Revenue YoY %, MRR Growth Rate, Churn Rate | Trend indicators |
| Line Chart | Revenue with YTD overlay | Performance trend |
| Gauge | Retention Rate, Would Recommend % | Health indicators |

### **Subscription Performance Page**
| Visual | Measures | Purpose |
|--------|----------|---------|
| Line Chart | MRR over time with PM comparison | Revenue trend |
| Donut Chart | Subscriptions by status | Portfolio mix |
| Funnel | Total → Active → Renewed | Lifecycle funnel |
| Table | Plan breakdown with ARPU, churn | Plan comparison |

### **Customer Analytics Page**
| Visual | Measures | Purpose |
|--------|----------|---------|
| Treemap | Churn by Reason % | Churn drivers |
| Bar Chart | Acquisition channel performance | Marketing ROI |
| Scatter | ARPU vs Subscription Length | Customer value matrix |
| Cards | Avg Rating, Delivery Rating | Satisfaction KPIs |

### **Time Intelligence Page**
| Visual | Measures | Purpose |
|--------|----------|---------|
| Line Chart | Revenue with PY comparison (dual axis) | YoY trend |
| Matrix | Months as rows, YoY %, MoM % as values | Period analysis |
| Area Chart | Revenue YTD cumulative | Goal tracking |
| Waterfall | Revenue MoM Change by month | Growth decomposition |

---

