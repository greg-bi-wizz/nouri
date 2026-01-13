# Business Analysis Guide (Power BI) — NourishBox

This guide turns the NourishBox Power BI build plan into a **step-by-step, business-oriented** approach.
It explains **what to build**, **how to build it**, and—most importantly—**why each page exists** from an analytics and BI value perspective.

**Source of truth for this guide:** project context from `README.md` + `WORKFLOW.md` and the current dataset structure.

---

## 1) What you’re building (the “why”)

NourishBox is a subscription business with realistic patterns:
- **Recurring revenue + upgrades** (subscription history + monthly snapshots)
- **Seasonality** (New Year spikes in acquisition; summer/holiday delivery pauses)
- **Churn dynamics** (notably high churn for Jan–Feb cohorts)
- **Marketing attribution** (campaigns tied to orders)
- **Product mix + customer satisfaction** (order items + reviews)

A strong BI portfolio report should:
1. Make executives confident about **revenue health** (MRR, growth, plan mix)
2. Make growth teams confident about **acquisition efficiency** (CAC proxies, conversion rates, channel mix)
3. Make retention teams confident about **churn drivers & intervention timing**
4. Make product/ops teams confident about **experience quality** (delivery performance, ratings)

---

## 2) Dataset & analytical grains (what each table represents)

Understanding grain is the foundation of correct modeling and measures.

### Core tables
- **customers** (grain: 1 row per customer)
  - demographics + acquisition channel + New Year signup flag
- **customer_preferences** (grain: 1 row per customer)
  - dietary & beauty preferences, allergies, household size
- **subscriptions** (grain: 1 row per subscription record)
  - history including upgrades and cancellations
- **subscription_monthly** (grain: 1 row per subscription per month)
  - pre-modeled monthly snapshot designed for **MRR/NRR-like** metrics
- **orders** (grain: 1 row per order/month delivery)
  - actual billed amount, discounts, shipping, delivery status, optional campaign attribution
- **order_items** (grain: 1 row per line item)
  - product-level detail + line pricing + discounts
- **marketing_campaigns** (grain: 1 row per campaign)
  - campaign metrics (budget, impressions, clicks, conversions)
- **reviews** (grain: 1 row per review)
  - ratings and feedback on delivered orders
- **churn_events** (grain: 1 row per churn event)
  - churn reasons and retention attempt outcomes

### Dimensions
- **plan_dim** (grain: 1 row per subscription plan)
- **date_dim** (grain: 1 row per date)

---

## 3) Step-by-step: from data → cloud → Power BI

### Step 3.1 — Generate the data locally
**Why:** guarantees reproducible portfolio results; you can tweak assumptions (customer count, seasonality) to demonstrate modeling skill.

Run:
```bash
python src/generate_nourishbox_data.py
```
Output is written to:
- `data/nourishbox/*.csv`


### Step 3.2 — Sync the data into Supabase (recommended)
**Why:** a cloud PostgreSQL source is a portfolio upgrade:
- demonstrates data engineering workflow
- enables “realistic” BI connectivity
- supports scheduled refresh in Power BI Service (depending on setup)

Run (fresh start):
```bash
python src/sync_to_supabase.py --clear
```

If credentials aren’t set, run setup:
```bash
python src/sync_to_supabase.py --setup
```


### Step 3.3 — Connect Power BI to Supabase (PostgreSQL)
**Why:** centralizes the data model and makes dashboards refreshable.

In Power BI Desktop:
1. **Get Data → PostgreSQL database**
2. Server: `db.<project-ref>.supabase.co` (from Supabase Settings → Database)
3. Database: `postgres`
4. Choose:
   - **Import** (recommended for portfolio responsiveness)
   - **DirectQuery** (only if you explicitly want “live” behavior; usually slower + more restrictions)

Tables to load (minimum viable model):
- customers
- customer_preferences
- subscriptions
- subscription_monthly
- orders
- order_items
- product_catalog
- plan_dim
- date_dim
- marketing_campaigns
- reviews
- churn_events

---

## 4) Power Query (Transform) setup

### Step 4.1 — Enforce data types
**Why:** correct types prevent subtle DAX errors and ensure time intelligence works.

Recommended types:
- IDs: Text
- Dates: Date
- Amounts (MRR, revenue, discounts, prices): Decimal number
- Flags (is_new_year_signup, auto_renew, active, would_recommend): True/False

### Step 4.2 — Basic cleaning rules
**Why:** keeps reports stable and consistent.

- Replace blanks in text fields with “(Unknown)” where useful (e.g., campaign attribution)
- Ensure `year_month` is Text (YYYY-MM) for labeling; use Date for calculations

---

## 5) Data model (relationships) — the most important step

**Why this matters:** almost every BI mistake comes from incorrect relationships or mixing grains.

Recommended relationships (single direction unless you have a strong reason otherwise):

### Core relationships
- customers[customer_id] → subscriptions[customer_id] (1:* )
- customers[customer_id] → customer_preferences[customer_id] (1:1)
- subscriptions[subscription_id] → orders[subscription_id] (1:* )
- orders[order_id] → order_items[order_id] (1:* )
- orders[order_id] → reviews[order_id] (1:* )
- subscriptions[subscription_id] → churn_events[subscription_id] (1:* )

### Dimensions
- plan_dim[plan_key] → subscriptions[plan_type] (1:* )
- plan_dim[plan_key] → orders[plan_type_at_order] (1:* )

### Dates
Pick one approach:

**Option A (recommended):** use date_dim for daily analysis
- date_dim[date_key] → orders[order_date_key] (1:* )

And for subscription snapshots:
- date_dim[date] → subscription_monthly[month_start] (1:* )

**Option B:** create a dedicated Month dimension for month_start analysis
- Only needed if you want a cleaner “month-only” table.

### Marketing attribution
- marketing_campaigns[campaign_id] → orders[campaign_id] (1:* )

---

## 6) Measures: a practical starter set

**Why:** measures turn raw tables into decision-ready KPIs.

Create a dedicated measure table (optional but recommended), e.g. `Core Measures`.

### Revenue & orders
- **Total Revenue**: sum of orders[order_total] for delivered/pending/delayed (exclude cancelled if appropriate)
- **Orders**: distinctcount(orders[order_id])
- **AOV**: [Total Revenue] / [Orders]
- **Discount $**: sum(orders[discount_applied])
- **Discount Rate**: [Discount $] / ([Total Revenue] + [Discount $]) (depending on your definition)

### Subscription economics
Use `subscription_monthly` for recurring metrics.
- **MRR**: sum(subscription_monthly[mrr])
- **Active Subscribers**: distinctcount(subscription_monthly[subscription_id]) filtered to status in {active, upgraded}
- **ARPU**: [MRR] / [Active Subscribers]

### Churn & retention
- **Churned Customers**: distinctcount(churn_events[customer_id])
- **Churn Rate (simple)**: [Churned Customers] / distinctcount(customers[customer_id])
- **New Year Churn Rate**: compare churn for customers[is_new_year_signup] = TRUE vs FALSE

### Marketing
- **Spend**: sum(marketing_campaigns[budget])
- **Conversions**: sum(marketing_campaigns[conversions])
- **CPA**: [Spend] / [Conversions]

> Note: marketing attribution in this dataset is “occasional campaign attribution” on orders.
> Treat campaign-to-order views as directional insights, not perfect attribution.

---

## 7) Page-by-page build plan (with BI rationale)

This section is the heart of the portfolio report. Each page has:
- **Analytical objective** (what decisions it supports)
- **Recommended visuals** (what to place)
- **Business value** (why it matters)


### Page 1 — Executive Overview
**Analytical objective:** a 30-second view of business health.

**Recommended visuals**
- KPI cards: **MRR**, **Total Revenue**, **Active Subscribers**, **Churn Rate**, **AOV**
- Line chart: MRR trend (with seasonal context)
- Stacked bar: revenue by plan category (meals / beauty / combo)
- Small multiples or sparkline KPIs: last 12 months
- Slicers: Year, Plan category, Acquisition channel

**Business value**
- Aligns leadership on whether the business is growing, stable, or declining
- Detects seasonality (January surge) and operational dips (summer/holiday pauses)
- Enables fast “where should we look next?” drilldown


### Page 2 — Revenue & MRR Deep Dive
**Analytical objective:** separate expected recurring revenue from realized revenue and identify drivers.

**Recommended visuals**
- Line chart: **MRR** (subscription_monthly) vs **Actual Revenue** (orders)
- Waterfall: month-over-month MRR change (new vs churn vs expansion — simplified)
- Matrix: MRR by plan tier (Meal Basic → Combo Deluxe)
- Histogram: order totals (AOV distribution)

**Business value**
- Shows whether revenue performance is subscription-driven vs discount/shipping-driven
- Highlights plan tiers that contribute most to stability
- Provides the foundation for forecasting and target setting


### Page 3 — Customer Acquisition & Segmentation
**Analytical objective:** understand who is joining, when, and through which channels.

**Recommended visuals**
- Line chart: new customers by month (show January/February spike)
- Bar chart: customers by acquisition channel
- Scatter or matrix: channel volume vs churn rate (or channel volume vs ARPU)
- Map: customers by state/city (optional)

**Business value**
- Helps prioritize acquisition investment (channels that bring durable customers)
- Exposes “high-volume but low-quality” channels
- Provides context for the New Year cohort (marketing timing vs retention risk)


### Page 4 — Retention, Cohorts & Churn Drivers
**Analytical objective:** identify when customers churn and why; find intervention windows.

**Recommended visuals**
- Cohort heatmap: retention by registration month (especially Jan/Feb vs others)
- Line chart: retention curve (New Year vs non-New Year cohorts)
- Bar chart: churn reasons distribution
- Funnel or KPI cards: retention offer attempted vs accepted

**Business value**
- Pinpoints the “month 2–3 cliff” for resolution signups
- Supports targeted retention playbooks (education, habit formation, plan downgrade offers)
- Connects qualitative churn reasons to quantitative churn rates


### Page 5 — Marketing ROI & Campaign Performance
**Analytical objective:** evaluate campaign efficiency (cost, conversion, and downstream impact where available).

**Recommended visuals**
- Table: campaigns with budget, impressions, clicks, conversions, CPA
- Bar chart: CPA by campaign type
- Trend: spend and conversions over time
- (Optional) attributed revenue from campaign-linked orders

**Business value**
- Moves marketing discussions from clicks to efficiency metrics
- Identifies campaign types with the best cost-to-growth balance
- Supports reallocation decisions (scale what works, fix or stop what doesn’t)


### Page 6 — Product & Plan Performance
**Analytical objective:** understand what customers receive, what they like, and where cross-sell opportunities exist.

**Recommended visuals**
- Top products by revenue/volume (from order_items)
- Product mix over time: meal vs beauty share
- Breakdown by preferences: dietary_preferences vs meal popularity
- Cross-sell proxy: plan category share + upgrades in subscriptions

**Business value**
- Connects operational choices (catalog) to financial outcomes (revenue, retention)
- Identifies which product categories drive engagement
- Supports merchandising decisions and bundle strategy


### Page 7 — Customer Experience (Reviews)
**Analytical objective:** quantify satisfaction, detect quality issues, and link experience to retention.

**Recommended visuals**
- KPI: average rating + % would recommend
- Rating distribution (1–5)
- Trends: rating over time and by delivery status
- Breakdown: meal_quality vs beauty_quality vs delivery_rating

**Business value**
- Early warning signals for churn (declining experience)
- Pinpoints whether issues are product quality or delivery execution
- Gives a narrative layer that complements financial charts


### Page 8 — Operations & Delivery Performance
**Analytical objective:** validate service reliability and its relationship to customer satisfaction.

**Recommended visuals**
- Delivery status trend: delivered vs delayed vs cancelled
- Delay rate by month (seasonality-aware)
- Correlation view: delays vs ratings (or delays vs churn)

**Business value**
- Helps ops teams prioritize reliability improvements
- Quantifies the business impact of logistics issues
- Supports staffing and vendor decisions during seasonal peaks

---

## 8) UX polish (portfolio-quality)

### Apply a theme
**Why:** consistent design makes dashboards feel professional.

If you use the included themes:
- Light theme: `powerbi/styles/nourishbox-theme.json`
- Dark theme: `powerbi/styles/nourishbox-theme-dark.json`

In Power BI Desktop:
- View → Themes → Browse for themes

### Add interactivity
**Why:** BI value increases when users can answer their own questions.

- Drill-through pages (e.g., customer detail, campaign detail)
- Tooltips for “explain the metric” and micro-trends
- Bookmarks to switch between “Executive / Analyst” views

---

## 9) Quality checks (don’t skip)

**Why:** these checks prevent incorrect conclusions.

- Validate totals:
  - orders sum(order_total) matches known ballpark (see README metrics)
- Validate MRR logic:
  - MRR uses subscription_monthly snapshot (not derived from orders)
- Validate relationships:
  - slicers filter visuals consistently

---

## 10) Suggested narrative for a portfolio README / interview

A good story arc:
1. “I modeled a subscription business with seasonality and churn dynamics.”
2. “I built a star-ish BI model with plan/date dimensions and monthly subscription snapshots.”
3. “My executive dashboard shows health, my retention page explains the New Year churn cliff, and my marketing page shows CPA-driven optimization.”
4. “I made the report interactive with drill-through and clear KPI definitions.”

---

## Appendix A — Recommended slicers (global)

- Year / Month
- Plan category (meals / beauty / combo)
- Acquisition channel
- New Year signup flag
- Delivery status

## Appendix B — Common pitfalls and how to avoid them

- **Mixing grains** (orders vs subscription_monthly): keep recurring revenue measures on snapshots, realized revenue on orders.
- **Many-to-many accidents**: ensure unique keys and correct relationship directions.
- **Wrong date table**: use `date_dim` for time intelligence; mark it as the Date table in Power BI.

## Appendix C — DAX measure definitions (starter pack)

These measures are designed to work with the current NourishBox schema:
- `subscription_monthly` (recurring snapshot: `month_start`, `mrr`, `status`, `subscription_id`)
- `orders` (realized revenue: `order_total`, `delivery_status`, `order_date`)
- `customers`, `churn_events`, `marketing_campaigns`, `reviews`

### C.1 Assumptions (recommended)

1. You have a calendar table:
   - Use `date_dim` and mark it as the Date table (Model view → right-click `date_dim` → *Mark as date table*).
2. Relationships:
   - `date_dim[date]` → `subscription_monthly[month_start]`
   - `date_dim[date]` → `orders[order_date]`
3. You have a dedicated measure table (optional): `Core Measures`.

> Tip: If your `date_dim` uses a different column name (some versions use `calendar_date`), update the DAX to match your model.

---

### C.2 Revenue & order measures

**Total Revenue (delivered + in-flight)**
```DAX
Total Revenue :=
CALCULATE(
  SUM(orders[order_total]),
  KEEPFILTERS(orders[delivery_status] IN { "delivered", "pending", "delayed" })
)
```

**Delivered Revenue (strict)**
```DAX
Delivered Revenue :=
CALCULATE(
  SUM(orders[order_total]),
  KEEPFILTERS(orders[delivery_status] = "delivered")
)
```

**Orders**
```DAX
Orders :=
DISTINCTCOUNT(orders[order_id])
```

**AOV**
```DAX
AOV :=
DIVIDE([Total Revenue], [Orders])
```

**Discount $**
```DAX
Discount $ :=
SUM(orders[discount_applied])
```

**Shipping $**
```DAX
Shipping $ :=
SUM(orders[shipping_cost])
```

---

### C.3 Subscription economics (MRR, active base)

**MRR** (use snapshots; avoids rebuilding logic from subscription start/end dates)
```DAX
MRR :=
SUM(subscription_monthly[mrr])
```

**Active Subscribers**
```DAX
Active Subscribers :=
CALCULATE(
  DISTINCTCOUNT(subscription_monthly[subscription_id]),
  KEEPFILTERS(subscription_monthly[status] IN { "active", "upgraded" })
)
```

**ARPU (MRR / active subscribers)**
```DAX
ARPU :=
DIVIDE([MRR], [Active Subscribers])
```

**ARR (run rate)**
```DAX
ARR :=
[MRR] * 12
```

**MRR MoM %**
```DAX
MRR MoM % :=
VAR PrevMRR = CALCULATE([MRR], DATEADD(date_dim[date], -1, MONTH))
RETURN DIVIDE([MRR] - PrevMRR, PrevMRR)
```

---

### C.4 Churn & retention measures (simple, portfolio-friendly)

**Churned Customers**
```DAX
Churned Customers :=
DISTINCTCOUNT(churn_events[customer_id])
```

**Total Customers**
```DAX
Total Customers :=
DISTINCTCOUNT(customers[customer_id])
```

**Churn Rate (simple)**
```DAX
Churn Rate (Simple) :=
DIVIDE([Churned Customers], [Total Customers])
```

**Churned Customers (New Year signups)**
```DAX
Churned Customers (New Year) :=
CALCULATE(
  DISTINCTCOUNT(churn_events[customer_id]),
  KEEPFILTERS(customers[is_new_year_signup] = TRUE())
)
```

**Churn Rate (New Year signups)**
```DAX
Churn Rate (New Year) :=
DIVIDE(
  [Churned Customers (New Year)],
  CALCULATE([Total Customers], KEEPFILTERS(customers[is_new_year_signup] = TRUE()))
)
```

> Analytical note: this is a *coarse* churn rate (share of customers who ever churned). For time-based churn (monthly logo churn), you’d compute churned base per month using `subscription_monthly` and churn dates.

---

### C.5 Marketing measures

**Marketing Spend**
```DAX
Marketing Spend :=
SUM(marketing_campaigns[budget])
```

**Marketing Conversions**
```DAX
Marketing Conversions :=
SUM(marketing_campaigns[conversions])
```

**CPA**
```DAX
CPA :=
DIVIDE([Marketing Spend], [Marketing Conversions])
```

**Attributed Revenue (order-linked campaigns)**
```DAX
Attributed Revenue :=
CALCULATE(
  [Total Revenue],
  KEEPFILTERS(NOT ISBLANK(orders[campaign_id]))
)
```

> Analytical note: campaign attribution is partial in this dataset (not every order has a campaign), so treat this as directional.

---

### C.6 Customer experience (reviews) measures

**Average Rating**
```DAX
Average Rating :=
AVERAGE(reviews[rating])
```

**Reviews**
```DAX
Reviews :=
DISTINCTCOUNT(reviews[review_id])
```

**% Would Recommend**
```DAX
% Would Recommend :=
DIVIDE(
  CALCULATE(COUNTROWS(reviews), KEEPFILTERS(reviews[would_recommend] = TRUE())),
  COUNTROWS(reviews)
)
```

---

### C.7 Operational measures (delivery performance)

**Delayed Orders**
```DAX
Delayed Orders :=
CALCULATE(
  [Orders],
  KEEPFILTERS(orders[delivery_status] = "delayed")
)
```

**Delay Rate**
```DAX
Delay Rate :=
DIVIDE([Delayed Orders], [Orders])
```


