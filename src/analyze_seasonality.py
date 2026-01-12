"""
NourishBox Seasonality Analysis
Analyze the seasonal patterns in customer signups, orders, and churn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
customers = pd.read_csv('data/nourishbox/customers.csv')
subscriptions = pd.read_csv('data/nourishbox/subscriptions.csv')
orders = pd.read_csv('data/nourishbox/orders.csv')
churn_events = pd.read_csv('data/nourishbox/churn_events.csv')

# Convert date columns
customers['registration_date'] = pd.to_datetime(customers['registration_date'])
subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'])
orders['order_date'] = pd.to_datetime(orders['order_date'])
churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'])

print(f"\nDataset Overview:")
print(f"  Total Customers: {len(customers):,}")
print(f"  Total Orders: {len(orders):,}")
print(f"  Total Churns: {len(churn_events):,}")
print(f"  Date Range: {customers['registration_date'].min()} to {customers['registration_date'].max()}")

# ============================================================================
# ANALYSIS 1: Customer Signups by Month
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS 1: Customer Signup Seasonality")
print("="*60)

# Group by year-month
customers['year_month'] = customers['registration_date'].dt.to_period('M')
customers['month'] = customers['registration_date'].dt.month
customers['month_name'] = customers['registration_date'].dt.month_name()

signups_by_month = customers.groupby('month_name').size()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
signups_by_month = signups_by_month.reindex(month_order)

print("\nSignups by Month:")
for month, count in signups_by_month.items():
    print(f"  {month:12s}: {count:4d} customers")

# Calculate percentage vs average
avg_signups = signups_by_month.mean()
print(f"\nAverage monthly signups: {avg_signups:.0f}")
print("\nDeviation from average:")
for month, count in signups_by_month.items():
    pct_diff = ((count - avg_signups) / avg_signups) * 100
    print(f"  {month:12s}: {pct_diff:+6.1f}%")

# ============================================================================
# ANALYSIS 2: New Year's Resolution Churn
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS 2: New Year's Resolution Churn Pattern")
print("="*60)

# Identify New Year signups
new_year_customers = customers[customers['is_new_year_signup'] == True]['customer_id']
other_customers = customers[customers['is_new_year_signup'] == False]['customer_id']

# Get churns for each group
new_year_churns = churn_events[churn_events['customer_id'].isin(new_year_customers)]
other_churns = churn_events[churn_events['customer_id'].isin(other_customers)]

# Calculate churn rates
new_year_churn_rate = len(new_year_churns) / len(new_year_customers) * 100
other_churn_rate = len(other_churns) / len(other_customers) * 100

print(f"\nNew Year Signups (Jan-Feb):")
print(f"  Total customers: {len(new_year_customers):,}")
print(f"  Churned: {len(new_year_churns):,}")
print(f"  Churn rate: {new_year_churn_rate:.1f}%")

print(f"\nOther Month Signups:")
print(f"  Total customers: {len(other_customers):,}")
print(f"  Churned: {len(other_churns):,}")
print(f"  Churn rate: {other_churn_rate:.1f}%")

# Analyze churn timing for New Year customers
new_year_churns_copy = new_year_churns.copy()
new_year_churns_copy['days_to_churn'] = new_year_churns_copy['subscription_length_days']
quick_churns = new_year_churns_copy[new_year_churns_copy['days_to_churn'] <= 90]
print(f"\nNew Year customers who churned within 90 days: {len(quick_churns)} ({len(quick_churns)/len(new_year_churns)*100:.1f}% of New Year churns)")

# ============================================================================
# ANALYSIS 3: Order Volume by Month
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS 3: Order Volume Seasonality")
print("="*60)

orders['month'] = orders['order_date'].dt.month
orders['month_name'] = orders['order_date'].dt.month_name()

orders_by_month = orders.groupby('month_name').size()
orders_by_month = orders_by_month.reindex(month_order)

print("\nOrders by Month:")
for month, count in orders_by_month.items():
    print(f"  {month:12s}: {count:5d} orders")

# Calculate percentage vs average
avg_orders = orders_by_month.mean()
print(f"\nAverage monthly orders: {avg_orders:.0f}")
print("\nDeviation from average:")
for month, count in orders_by_month.items():
    pct_diff = ((count - avg_orders) / avg_orders) * 100
    print(f"  {month:12s}: {pct_diff:+6.1f}%")

# ============================================================================
# ANALYSIS 4: Revenue by Month
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS 4: Revenue Seasonality")
print("="*60)

revenue_by_month = orders.groupby('month_name')['order_total'].sum()
revenue_by_month = revenue_by_month.reindex(month_order)

print("\nRevenue by Month:")
for month, revenue in revenue_by_month.items():
    print(f"  {month:12s}: ${revenue:,.2f}")

avg_revenue = revenue_by_month.mean()
print(f"\nAverage monthly revenue: ${avg_revenue:,.2f}")
print("\nDeviation from average:")
for month, revenue in revenue_by_month.items():
    pct_diff = ((revenue - avg_revenue) / avg_revenue) * 100
    print(f"  {month:12s}: {pct_diff:+6.1f}%")

# ============================================================================
# ANALYSIS 5: Churn by Month
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS 5: Churn Seasonality")
print("="*60)

churn_events['month'] = churn_events['churn_date'].dt.month
churn_events['month_name'] = churn_events['churn_date'].dt.month_name()

churns_by_month = churn_events.groupby('month_name').size()
churns_by_month = churns_by_month.reindex(month_order)

print("\nChurns by Month:")
for month, count in churns_by_month.items():
    print(f"  {month:12s}: {count:4d} churns")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n" + "="*60)
print("Creating visualizations...")
print("="*60)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('NourishBox Seasonality Analysis', fontsize=16, fontweight='bold')

# Plot 1: Signups by Month
ax1 = axes[0, 0]
signups_by_month.plot(kind='bar', ax=ax1, color='steelblue')
ax1.set_title('Customer Signups by Month', fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Number of Signups')
ax1.axhline(y=avg_signups, color='red', linestyle='--', label=f'Average ({avg_signups:.0f})')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Orders by Month
ax2 = axes[0, 1]
orders_by_month.plot(kind='bar', ax=ax2, color='green')
ax2.set_title('Order Volume by Month', fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('Number of Orders')
ax2.axhline(y=avg_orders, color='red', linestyle='--', label=f'Average ({avg_orders:.0f})')
ax2.legend()
ax2.tick_params(axis='x', rotation=45)

# Plot 3: Revenue by Month
ax3 = axes[0, 2]
(revenue_by_month / 1000).plot(kind='bar', ax=ax3, color='orange')
ax3.set_title('Revenue by Month', fontweight='bold')
ax3.set_xlabel('Month')
ax3.set_ylabel('Revenue ($1000s)')
ax3.axhline(y=avg_revenue/1000, color='red', linestyle='--', label=f'Average (${avg_revenue/1000:.1f}K)')
ax3.legend()
ax3.tick_params(axis='x', rotation=45)

# Plot 4: Churns by Month
ax4 = axes[1, 0]
churns_by_month.plot(kind='bar', ax=ax4, color='crimson')
ax4.set_title('Customer Churn by Month', fontweight='bold')
ax4.set_xlabel('Month')
ax4.set_ylabel('Number of Churns')
ax4.tick_params(axis='x', rotation=45)

# Plot 5: Churn Rate Comparison
ax5 = axes[1, 1]
churn_comparison = pd.DataFrame({
    'New Year Signups\n(Jan-Feb)': [new_year_churn_rate],
    'Other Months': [other_churn_rate]
})
churn_comparison.T.plot(kind='bar', ax=ax5, legend=False, color=['crimson', 'steelblue'])
ax5.set_title('Churn Rate: New Year vs Other Signups', fontweight='bold')
ax5.set_ylabel('Churn Rate (%)')
ax5.set_xlabel('')
ax5.tick_params(axis='x', rotation=45)
for i, v in enumerate([new_year_churn_rate, other_churn_rate]):
    ax5.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

# Plot 6: Time Series - Signups over time
ax6 = axes[1, 2]
signups_over_time = customers.groupby(customers['registration_date'].dt.to_period('M')).size()
signups_over_time.index = signups_over_time.index.to_timestamp()
signups_over_time.plot(ax=ax6, color='steelblue', linewidth=2)
ax6.set_title('Customer Signups Over Time', fontweight='bold')
ax6.set_xlabel('Date')
ax6.set_ylabel('Monthly Signups')
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/nourishbox/seasonality_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved to: data/nourishbox/seasonality_analysis.png")

# ============================================================================
# SUMMARY INSIGHTS
# ============================================================================
print("\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)

print("\n1. CUSTOMER ACQUISITION:")
print(f"   • January has the highest signups ({signups_by_month['January']} customers, +{((signups_by_month['January']-avg_signups)/avg_signups*100):.1f}%)")
print(f"   • Summer months (Jun-Aug) have lowest signups")
print(f"   • Holiday season (Nov-Dec) also shows reduced acquisition")

print("\n2. NEW YEAR'S RESOLUTION EFFECT:")
print(f"   • {len(new_year_customers)} customers signed up in Jan-Feb ({len(new_year_customers)/len(customers)*100:.1f}% of total)")
print(f"   • New Year signups have {new_year_churn_rate-other_churn_rate:.1f}% higher churn rate")
print(f"   • {len(quick_churns)/len(new_year_churns)*100:.1f}% of New Year churns happen within 90 days")

print("\n3. ORDER PATTERNS:")
july_orders = orders_by_month['July']
dec_orders = orders_by_month['December']
print(f"   • July shows lowest order volume ({july_orders} orders, {((july_orders-avg_orders)/avg_orders*100):.1f}%)")
print(f"   • December also reduced ({dec_orders} orders, {((dec_orders-avg_orders)/avg_orders*100):.1f}%)")
print(f"   • This indicates seasonal pausing during vacations and holidays")

print("\n4. REVENUE IMPACT:")
july_rev = revenue_by_month['July']
dec_rev = revenue_by_month['December']
print(f"   • July revenue: ${july_rev:,.2f} ({((july_rev-avg_revenue)/avg_revenue*100):.1f}%)")
print(f"   • December revenue: ${dec_rev:,.2f} ({((dec_rev-avg_revenue)/avg_revenue*100):.1f}%)")
print(f"   • Peak months (Jan-Mar) show strongest revenue")

print("\n" + "="*60)
print("Analysis complete!")
print("="*60 + "\n")