# NourishBox Power BI Measures - Comprehensive Suggestions

## Current Measures
- Total Revenue: `SUM(orders[order_total])`
- Active Subscriptions: `CALCULATE(COUNTROWS(subscriptions), subscriptions[status] = "active")`

---

## 1. Revenue Metrics

### Monthly Recurring Revenue (MRR)
```dax
MRR = 
CALCULATE(
    SUM(subscriptions[monthly_price]),
    subscriptions[status] = "active"
)
```

### MRR Growth Rate
```dax
MRR Growth Rate = 
VAR CurrentMRR = [MRR]
VAR PreviousMRR = CALCULATE([MRR], DATEADD('orders'[order_date], -1, MONTH))
RETURN
DIVIDE(CurrentMRR - PreviousMRR, PreviousMRR, 0)
```

### Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE(
    [Total Revenue],
    COUNTROWS(orders),
    0
)
```

### Revenue After Discount
```dax
Revenue After Discount = 
SUMX(
    orders,
    orders[order_total] - orders[discount_applied]
)
```

### Discount Impact %
```dax
Discount Impact % = 
DIVIDE(
    SUM(orders[discount_applied]),
    [Total Revenue],
    0
)
```

### Revenue by Plan Type
```dax
Revenue by Plan = 
CALCULATE(
    [Total Revenue],
    ALLEXCEPT(subscriptions, subscriptions[plan_type])
)
```

### Shipping Revenue
```dax
Shipping Revenue = SUM(orders[shipping_cost])
```

---

## 2. Customer Metrics

### Total Customers
```dax
Total Customers = DISTINCTCOUNT(customers[customer_id])
```

### New Customers
```dax
New Customers = 
CALCULATE(
    DISTINCTCOUNT(customers[customer_id]),
    customers[registration_date] >= MIN(orders[order_date]) &&
    customers[registration_date] <= MAX(orders[order_date])
)
```

### Customer Lifetime Value (CLV)
```dax
Customer Lifetime Value = 
AVERAGEX(
    VALUES(customers[customer_id]),
    CALCULATE([Total Revenue])
)
```

### Average Customer Age
```dax
Average Customer Age = AVERAGE(customers[age])
```

### Referral Customers Count
```dax
Referral Customers = 
CALCULATE(
    COUNTROWS(customers),
    NOT(ISBLANK(customers[referred_by_customer_id]))
)
```

### Referral Rate %
```dax
Referral Rate % = 
DIVIDE(
    [Referral Customers],
    [Total Customers],
    0
)
```

---

## 3. Subscription Metrics

### Total Subscriptions
```dax
Total Subscriptions = COUNTROWS(subscriptions)
```

### Cancelled Subscriptions
```dax
Cancelled Subscriptions = 
CALCULATE(
    COUNTROWS(subscriptions),
    subscriptions[status] = "cancelled"
)
```

### Upgraded Subscriptions
```dax
Upgraded Subscriptions = 
CALCULATE(
    COUNTROWS(subscriptions),
    subscriptions[status] = "upgraded"
)
```

### Subscription Retention Rate %
```dax
Retention Rate % = 
DIVIDE(
    [Active Subscriptions],
    [Active Subscriptions] + [Cancelled Subscriptions],
    0
)
```

### Average Subscription Length (Days)
```dax
Avg Subscription Length = 
AVERAGE(churn_events[subscription_length_days])
```

### Auto-Renew Rate %
```dax
Auto Renew Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(subscriptions), subscriptions[auto_renew] = TRUE()),
    COUNTROWS(subscriptions),
    0
)
```

---

## 4. Churn Metrics

### Churn Count
```dax
Churn Count = COUNTROWS(churn_events)
```

### Churn Rate %
```dax
Churn Rate % = 
DIVIDE(
    [Churn Count],
    [Total Subscriptions],
    0
)
```

### Monthly Churn Rate %
```dax
Monthly Churn Rate % = 
VAR TotalActive = [Active Subscriptions]
VAR ChurnedThisMonth = 
    CALCULATE(
        COUNTROWS(churn_events),
        DATESMTD(churn_events[churn_date])
    )
RETURN
DIVIDE(ChurnedThisMonth, TotalActive + ChurnedThisMonth, 0)
```

### Retention Offer Success Rate %
```dax
Retention Success Rate % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(churn_events),
        churn_events[retention_offer_accepted] = TRUE()
    ),
    CALCULATE(
        COUNTROWS(churn_events),
        churn_events[attempted_retention] = TRUE()
    ),
    0
)
```

### Average Days to Churn
```dax
Avg Days to Churn = 
AVERAGE(churn_events[subscription_length_days])
```

### Churn Feedback Rate %
```dax
Churn Feedback Rate % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(churn_events),
        churn_events[feedback_provided] = TRUE()
    ),
    [Churn Count],
    0
)
```

---

## 5. Order & Delivery Metrics

### Total Orders
```dax
Total Orders = COUNTROWS(orders)
```

### Orders Delivered
```dax
Orders Delivered = 
CALCULATE(
    COUNTROWS(orders),
    orders[delivery_status] = "delivered"
)
```

### On-Time Delivery Rate %
```dax
On Time Delivery % = 
DIVIDE(
    [Orders Delivered],
    [Total Orders],
    0
)
```

### Delayed Orders
```dax
Delayed Orders = 
CALCULATE(
    COUNTROWS(orders),
    orders[delivery_status] = "delayed"
)
```

### Cancelled Orders
```dax
Cancelled Orders = 
CALCULATE(
    COUNTROWS(orders),
    orders[delivery_status] = "cancelled"
)
```

### Average Shipping Cost
```dax
Avg Shipping Cost = AVERAGE(orders[shipping_cost])
```

### Orders per Customer
```dax
Orders per Customer = 
DIVIDE(
    [Total Orders],
    [Total Customers],
    0
)
```

---

## 6. Review & Satisfaction Metrics

### Total Reviews
```dax
Total Reviews = COUNTROWS(reviews)
```

### Average Rating
```dax
Average Rating = AVERAGE(reviews[rating])
```

### Average Meal Quality Rating
```dax
Avg Meal Quality = AVERAGE(reviews[meal_quality_rating])
```

### Average Beauty Quality Rating
```dax
Avg Beauty Quality = AVERAGE(reviews[beauty_quality_rating])
```

### Average Delivery Rating
```dax
Avg Delivery Rating = AVERAGE(reviews[delivery_rating])
```

### Average Value Rating
```dax
Avg Value Rating = AVERAGE(reviews[value_rating])
```

### Recommendation Rate %
```dax
Recommendation Rate % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(reviews),
        reviews[would_recommend] = TRUE()
    ),
    [Total Reviews],
    0
)
```

### Review Response Rate %
```dax
Review Response Rate % = 
DIVIDE(
    [Total Reviews],
    [Total Orders],
    0
)
```

### 5-Star Reviews Count
```dax
5 Star Reviews = 
CALCULATE(
    COUNTROWS(reviews),
    reviews[rating] = 5
)
```

### 1-2 Star Reviews Count
```dax
Low Rating Reviews = 
CALCULATE(
    COUNTROWS(reviews),
    reviews[rating] <= 2
)
```

---

## 7. Product Metrics

### Total Order Items
```dax
Total Order Items = COUNTROWS(order_items)
```

### Meal Items Count
```dax
Meal Items = 
CALCULATE(
    COUNTROWS(order_items),
    order_items[product_type] = "meal"
)
```

### Beauty Items Count
```dax
Beauty Items = 
CALCULATE(
    COUNTROWS(order_items),
    order_items[product_type] = "beauty"
)
```

### Meal to Beauty Ratio
```dax
Meal to Beauty Ratio = 
DIVIDE(
    [Meal Items],
    [Beauty Items],
    0
)
```

### Average Items per Order
```dax
Avg Items per Order = 
DIVIDE(
    [Total Order Items],
    [Total Orders],
    0
)
```

### Total Unit Cost
```dax
Total Unit Cost = SUM(order_items[unit_cost])
```

### Gross Margin
```dax
Gross Margin = 
[Total Revenue] - [Total Unit Cost]
```

### Gross Margin %
```dax
Gross Margin % = 
DIVIDE(
    [Gross Margin],
    [Total Revenue],
    0
)
```

---

## 8. Marketing Metrics

### Total Marketing Budget
```dax
Marketing Budget = SUM(marketing_campaigns[budget])
```

### Total Campaign Impressions
```dax
Total Impressions = SUM(marketing_campaigns[impressions])
```

### Total Campaign Clicks
```dax
Total Clicks = SUM(marketing_campaigns[clicks])
```

### Total Conversions
```dax
Total Conversions = SUM(marketing_campaigns[conversions])
```

### Overall CTR %
```dax
Overall CTR % = 
DIVIDE(
    [Total Clicks],
    [Total Impressions],
    0
)
```

### Overall Conversion Rate %
```dax
Overall Conversion Rate % = 
DIVIDE(
    [Total Conversions],
    [Total Clicks],
    0
)
```

### Average Cost per Acquisition (CAC)
```dax
Average CAC = 
DIVIDE(
    [Marketing Budget],
    [Total Conversions],
    0
)
```

### Marketing ROI
```dax
Marketing ROI = 
VAR RevenueFromConversions = [Total Conversions] * [Average Order Value]
RETURN
DIVIDE(
    RevenueFromConversions - [Marketing Budget],
    [Marketing Budget],
    0
)
```

### Cost per Click (CPC)
```dax
Cost per Click = 
DIVIDE(
    [Marketing Budget],
    [Total Clicks],
    0
)
```

### Active Campaigns Count
```dax
Active Campaigns = 
CALCULATE(
    COUNTROWS(marketing_campaigns),
    marketing_campaigns[end_date] >= TODAY()
)
```

---

## 9. Cohort & Time-Based Metrics

### Customer Acquisition Cost by Channel
```dax
CAC by Channel = 
DIVIDE(
    CALCULATE(
        [Marketing Budget],
        ALLEXCEPT(marketing_campaigns, marketing_campaigns[campaign_type])
    ),
    CALCULATE(
        [Total Conversions],
        ALLEXCEPT(marketing_campaigns, marketing_campaigns[campaign_type])
    ),
    0
)
```

### Revenue This Month
```dax
Revenue This Month = 
CALCULATE(
    [Total Revenue],
    DATESMTD(orders[order_date])
)
```

### Revenue Last Month
```dax
Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    DATEADD(orders[order_date], -1, MONTH)
)
```

### Revenue YoY Growth %
```dax
Revenue YoY Growth % = 
VAR CurrentYear = [Total Revenue]
VAR PreviousYear = CALCULATE([Total Revenue], DATEADD(orders[order_date], -1, YEAR))
RETURN
DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0)
```

### Cumulative Revenue
```dax
Cumulative Revenue = 
CALCULATE(
    [Total Revenue],
    FILTER(
        ALL(orders[order_date]),
        orders[order_date] <= MAX(orders[order_date])
    )
)
```

---

## 10. Advanced Analytical Metrics

### Customer Recency (Days)
```dax
Avg Customer Recency = 
AVERAGEX(
    VALUES(customers[customer_id]),
    DATEDIFF(
        CALCULATE(MAX(orders[order_date])),
        TODAY(),
        DAY
    )
)
```

### Customer Frequency
```dax
Customer Frequency = 
AVERAGEX(
    VALUES(customers[customer_id]),
    CALCULATE(COUNTROWS(orders))
)
```

### Customer Monetary Value
```dax
Customer Monetary Value = 
AVERAGEX(
    VALUES(customers[customer_id]),
    CALCULATE([Total Revenue])
)
```

### LTV to CAC Ratio
```dax
LTV to CAC Ratio = 
DIVIDE(
    [Customer Lifetime Value],
    [Average CAC],
    0
)
```

### Payback Period (Months)
```dax
Payback Period Months = 
DIVIDE(
    [Average CAC],
    [MRR] / [Active Subscriptions],
    0
)
```

### Revenue per Active Subscriber
```dax
Revenue per Active Subscriber = 
DIVIDE(
    [Total Revenue],
    [Active Subscriptions],
    0
)
```

### Customer Concentration Risk
```dax
Top 10 Customer Revenue % = 
VAR Top10Revenue = 
    CALCULATE(
        [Total Revenue],
        TOPN(
            10,
            VALUES(customers[customer_id]),
            [Total Revenue],
            DESC
        )
    )
RETURN
DIVIDE(Top10Revenue, [Total Revenue], 0)
```

---

## 11. Plan-Specific Metrics

### Meal Plan Subscribers
```dax
Meal Plan Subscribers = 
CALCULATE(
    [Active Subscriptions],
    subscriptions[plan_type] IN {"meal_basic", "meal_plus"}
)
```

### Beauty Plan Subscribers
```dax
Beauty Plan Subscribers = 
CALCULATE(
    [Active Subscriptions],
    subscriptions[plan_type] IN {"beauty_essentials", "beauty_premium"}
)
```

### Combo Plan Subscribers
```dax
Combo Plan Subscribers = 
CALCULATE(
    [Active Subscriptions],
    subscriptions[plan_type] IN {"combo_starter", "combo_deluxe"}
)
```

### Average Plan Price
```dax
Avg Plan Price = AVERAGE(subscriptions[monthly_price])
```

### Plan Upgrade Rate %
```dax
Plan Upgrade Rate % = 
DIVIDE(
    [Upgraded Subscriptions],
    [Total Subscriptions],
    0
)
```

---

## 12. Geographic Metrics

### Unique States Served
```dax
States Served = DISTINCTCOUNT(customers[state])
```

### Unique Cities Served
```dax
Cities Served = DISTINCTCOUNT(customers[city])
```

### Revenue per State
```dax
Revenue per State = 
DIVIDE(
    [Total Revenue],
    [States Served],
    0
)
```

---

## Implementation Priority

### High Priority (Core KPIs)
1. MRR
2. Churn Rate %
3. Customer Lifetime Value
4. Average Order Value
5. Average Rating
6. Gross Margin %

### Medium Priority (Operational Metrics)
1. On-Time Delivery %
2. Retention Success Rate %
3. Marketing ROI
4. Review Response Rate %
5. Plan Upgrade Rate %

### Lower Priority (Deep Analysis)
1. Customer Concentration Risk
2. Payback Period
3. LTV to CAC Ratio
4. Cohort-specific metrics

---

## Display Folders Recommendation

Organize measures in display folders:
- **Revenue**: All revenue-related measures
- **Customers**: Customer counts and metrics
- **Subscriptions**: Subscription status and metrics
- **Churn & Retention**: Churn and retention measures
- **Orders & Delivery**: Order and delivery metrics
- **Reviews & Satisfaction**: Review ratings and satisfaction
- **Products**: Product and inventory metrics
- **Marketing**: Campaign and acquisition metrics
- **Time Intelligence**: YoY, MoM, cumulative metrics
- **Advanced Analytics**: RFM, LTV, CAC ratios

---

## Notes on Implementation

1. **Date Table**: Ensure proper date table relationships for time intelligence functions
2. **Format Strings**: Apply appropriate formats (%, $, #) to each measure
3. **Descriptions**: Add descriptions to measures for documentation
4. **Testing**: Validate measures with known data points from README.md
5. **Performance**: Use variables in complex calculations to improve performance
6. **Incremental Builds**: Start with high-priority measures first

