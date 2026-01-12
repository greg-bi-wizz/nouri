"""
NourishBox Cohort Analysis
Analyze customer retention and behavior by signup cohort
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("coolwarm")

print("="*70)
print("NOURISHBOX COHORT ANALYSIS")
print("="*70)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\nLoading data...")
customers = pd.read_csv('data/nourishbox/customers.csv')
subscriptions = pd.read_csv('data/nourishbox/subscriptions.csv')
orders = pd.read_csv('data/nourishbox/orders.csv')

# Convert date columns
customers['registration_date'] = pd.to_datetime(customers['registration_date'])
orders['order_date'] = pd.to_datetime(orders['order_date'])
subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'])

print(f"✓ Loaded {len(customers):,} customers")
print(f"✓ Loaded {len(orders):,} orders")
print(f"✓ Loaded {len(subscriptions):,} subscriptions")

# ============================================================================
# PREPARE COHORT DATA
# ============================================================================
print("\nPreparing cohort data...")

# Define cohort for each customer (month of registration)
customers['cohort'] = customers['registration_date'].dt.to_period('M')

# Merge orders with customer cohort
orders_cohort = orders.merge(
    customers[['customer_id', 'cohort', 'is_new_year_signup']],
    on='customer_id',
    how='left'
)

# Calculate order period (months since registration)
orders_cohort['order_period'] = orders_cohort['order_date'].dt.to_period('M')

# Calculate period index early for all orders
orders_cohort['cohort_timestamp'] = orders_cohort['cohort'].dt.to_timestamp()
orders_cohort['order_timestamp'] = orders_cohort['order_period'].dt.to_timestamp()
orders_cohort['period_index'] = ((orders_cohort['order_timestamp'].dt.year - orders_cohort['cohort_timestamp'].dt.year) * 12 +
                                  (orders_cohort['order_timestamp'].dt.month - orders_cohort['cohort_timestamp'].dt.month))

# ============================================================================
# COHORT 1: RETENTION COHORT (Monthly Retention Rates)
# ============================================================================
print("\n" + "="*70)
print("COHORT ANALYSIS 1: Monthly Retention Rates")
print("="*70)

# For each customer, find their first order and subsequent orders
customer_first_order = orders.groupby('customer_id')['order_date'].min().reset_index()
customer_first_order.columns = ['customer_id', 'first_order_date']
customer_first_order['first_order_period'] = customer_first_order['first_order_date'].dt.to_period('M')

# Merge with customers
customers_with_first_order = customers.merge(customer_first_order, on='customer_id', how='left')

# For retention analysis, we need to track which customers had orders in each period
# Get all customer-period combinations where they had an order
customer_periods = orders_cohort.groupby(['customer_id', 'cohort', 'order_period']).size().reset_index(name='orders')

# Calculate period index (months since cohort start)
customer_periods['cohort_timestamp'] = customer_periods['cohort'].dt.to_timestamp()
customer_periods['order_timestamp'] = customer_periods['order_period'].dt.to_timestamp()
customer_periods['period_index'] = ((customer_periods['order_timestamp'].dt.year - customer_periods['cohort_timestamp'].dt.year) * 12 +
                                     (customer_periods['order_timestamp'].dt.month - customer_periods['cohort_timestamp'].dt.month))

# Create retention table
cohort_data = customer_periods.groupby(['cohort', 'period_index'])['customer_id'].nunique().reset_index()
cohort_data.columns = ['cohort', 'period_index', 'customers']

# Get cohort sizes (customers in month 0)
cohort_sizes = cohort_data[cohort_data['period_index'] == 0][['cohort', 'customers']]
cohort_sizes.columns = ['cohort', 'cohort_size']

# Merge to calculate retention percentages
cohort_data = cohort_data.merge(cohort_sizes, on='cohort', how='left')
cohort_data['retention'] = (cohort_data['customers'] / cohort_data['cohort_size']) * 100

# Pivot to create retention matrix
retention_matrix = cohort_data.pivot(index='cohort', columns='period_index', values='retention')

# Limit to first 12 months for better visualization
retention_matrix_12m = retention_matrix.iloc[:, :13]  # Month 0 to Month 12

print(f"\nRetention Matrix (first 12 months):")
print(f"Cohort format: YYYY-MM")
print(f"Values: % of cohort still active\n")

# Display sample of retention matrix
display_cohorts = retention_matrix_12m.head(10)
print(display_cohorts.round(1).to_string())

# ============================================================================
# COHORT 2: NEW YEAR VS OTHER COHORTS
# ============================================================================
print("\n" + "="*70)
print("COHORT ANALYSIS 2: New Year Signups vs Other Months")
print("="*70)

# Separate New Year cohorts
orders_cohort['cohort_type'] = orders_cohort['is_new_year_signup'].apply(
    lambda x: 'New Year (Jan-Feb)' if x else 'Other Months'
)

# Calculate retention by cohort type
customer_periods_type = orders_cohort.groupby(['customer_id', 'cohort_type', 'order_period']).size().reset_index(name='orders')

# Get first order period for each customer
first_orders_by_customer = orders_cohort.groupby('customer_id').agg({
    'order_date': 'min',
    'cohort_type': 'first'
}).reset_index()
first_orders_by_customer['first_period'] = first_orders_by_customer['order_date'].dt.to_period('M')

# Merge back to get period index
customer_periods_type = customer_periods_type.merge(
    first_orders_by_customer[['customer_id', 'first_period']],
    on='customer_id'
)

customer_periods_type['period_timestamp'] = customer_periods_type['order_period'].dt.to_timestamp()
customer_periods_type['first_timestamp'] = customer_periods_type['first_period'].dt.to_timestamp()
customer_periods_type['period_index'] = ((customer_periods_type['period_timestamp'].dt.year - customer_periods_type['first_timestamp'].dt.year) * 12 +
                                          (customer_periods_type['period_timestamp'].dt.month - customer_periods_type['first_timestamp'].dt.month))

# Create retention by type
retention_by_type = customer_periods_type.groupby(['cohort_type', 'period_index'])['customer_id'].nunique().reset_index()

# Get initial sizes
initial_sizes = retention_by_type[retention_by_type['period_index'] == 0][['cohort_type', 'customer_id']]
initial_sizes.columns = ['cohort_type', 'initial_size']

retention_by_type = retention_by_type.merge(initial_sizes, on='cohort_type')
retention_by_type['retention'] = (retention_by_type['customer_id'] / retention_by_type['initial_size']) * 100

# Pivot for comparison
retention_comparison = retention_by_type.pivot(index='period_index', columns='cohort_type', values='retention')
retention_comparison = retention_comparison.loc[:12]  # First 12 months

print("\nRetention Comparison: New Year vs Other Signups")
print("Month | New Year (Jan-Feb) | Other Months | Difference")
print("-" * 60)
for idx in range(min(13, len(retention_comparison))):
    ny_val = retention_comparison.loc[idx, 'New Year (Jan-Feb)'] if idx in retention_comparison.index else 0
    other_val = retention_comparison.loc[idx, 'Other Months'] if idx in retention_comparison.index else 0
    diff = ny_val - other_val
    print(f"  {idx:2d}  |      {ny_val:5.1f}%         |    {other_val:5.1f}%     |   {diff:+5.1f}%")

# ============================================================================
# COHORT 3: REVENUE COHORT ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("COHORT ANALYSIS 3: Revenue by Cohort")
print("="*70)

# Calculate revenue by cohort and period
revenue_cohort = orders_cohort.groupby(['cohort', 'period_index'])['order_total'].sum().reset_index()
revenue_cohort = revenue_cohort.merge(cohort_sizes, on='cohort', how='left')
revenue_cohort['revenue_per_customer'] = revenue_cohort['order_total'] / revenue_cohort['cohort_size']

# Pivot revenue matrix
revenue_matrix = revenue_cohort.pivot(index='cohort', columns='period_index', values='revenue_per_customer')
revenue_matrix_12m = revenue_matrix.iloc[:, :13]

print(f"\nAverage Revenue per Customer by Cohort (first 12 months):")
print(f"Values: $ per customer in cohort\n")
display_revenue = revenue_matrix_12m.head(10)
print(display_revenue.round(2).to_string())

# Calculate cumulative LTV
cumulative_revenue = revenue_matrix_12m.cumsum(axis=1)
print(f"\nCumulative Customer Lifetime Value (first 12 months):")
print(f"Values: Total $ per customer\n")
display_cumulative = cumulative_revenue.head(10)
print(display_cumulative.round(2).to_string())

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n" + "="*70)
print("Creating visualizations...")
print("="*70)

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# ============================================================================
# Plot 1: Retention Heatmap
# ============================================================================
ax1 = fig.add_subplot(gs[0, :])

# Use only cohorts with enough history (at least 6 months)
retention_matrix_plot = retention_matrix_12m.iloc[-20:]  # Last 20 cohorts

sns.heatmap(
    retention_matrix_plot,
    annot=True,
    fmt='.0f',
    cmap='RdYlGn',
    center=50,
    vmin=0,
    vmax=100,
    cbar_kws={'label': 'Retention %'},
    ax=ax1,
    linewidths=0.5,
    yticklabels=[str(x) for x in retention_matrix_plot.index]
)
ax1.set_title('Monthly Retention Rate by Cohort (%)\nMonth 0 = First Order',
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Months Since First Order', fontsize=12, fontweight='bold')
ax1.set_ylabel('Cohort (Registration Month)', fontsize=12, fontweight='bold')

# ============================================================================
# Plot 2: Retention Curve Comparison (New Year vs Others)
# ============================================================================
ax2 = fig.add_subplot(gs[1, 0])

retention_comparison.plot(ax=ax2, linewidth=3, marker='o', markersize=8)
ax2.set_title('Retention Curve: New Year vs Other Signups',
              fontsize=14, fontweight='bold')
ax2.set_xlabel('Months Since First Order', fontsize=11, fontweight='bold')
ax2.set_ylabel('Retention Rate (%)', fontsize=11, fontweight='bold')
ax2.legend(title='Cohort Type', fontsize=10, title_fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 105)

# Add annotations for key drop-off points
for col in retention_comparison.columns:
    if 3 in retention_comparison.index:
        month3_retention = retention_comparison.loc[3, col]
        ax2.annotate(f'{month3_retention:.1f}%',
                    xy=(3, month3_retention),
                    xytext=(3, month3_retention + 5),
                    fontsize=9, ha='center')

# ============================================================================
# Plot 3: Average Retention by Month
# ============================================================================
ax3 = fig.add_subplot(gs[1, 1])

avg_retention = retention_matrix_12m.mean(axis=0)
avg_retention.plot(kind='bar', ax=ax3, color='steelblue', width=0.7)
ax3.set_title('Average Retention Rate by Month',
              fontsize=14, fontweight='bold')
ax3.set_xlabel('Months Since First Order', fontsize=11, fontweight='bold')
ax3.set_ylabel('Average Retention (%)', fontsize=11, fontweight='bold')
ax3.tick_params(axis='x', rotation=0)
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, v in enumerate(avg_retention):
    if not pd.isna(v):
        ax3.text(i, v + 2, f'{v:.0f}%', ha='center', fontsize=9)

# ============================================================================
# Plot 4: Cumulative LTV Heatmap
# ============================================================================
ax4 = fig.add_subplot(gs[2, 0])

cumulative_revenue_plot = cumulative_revenue.iloc[-20:]

sns.heatmap(
    cumulative_revenue_plot,
    annot=True,
    fmt='.0f',
    cmap='YlGnBu',
    cbar_kws={'label': 'Cumulative Revenue ($)'},
    ax=ax4,
    linewidths=0.5,
    yticklabels=[str(x) for x in cumulative_revenue_plot.index]
)
ax4.set_title('Cumulative Customer Lifetime Value by Cohort ($)',
              fontsize=14, fontweight='bold', pad=20)
ax4.set_xlabel('Months Since First Order', fontsize=12, fontweight='bold')
ax4.set_ylabel('Cohort (Registration Month)', fontsize=12, fontweight='bold')

# ============================================================================
# Plot 5: LTV Curve
# ============================================================================
ax5 = fig.add_subplot(gs[2, 1])

avg_ltv = cumulative_revenue.mean(axis=0)
avg_ltv.plot(ax=ax5, linewidth=3, marker='o', markersize=8, color='green')
ax5.set_title('Average Customer Lifetime Value Over Time',
              fontsize=14, fontweight='bold')
ax5.set_xlabel('Months Since First Order', fontsize=11, fontweight='bold')
ax5.set_ylabel('Cumulative LTV ($)', fontsize=11, fontweight='bold')
ax5.grid(True, alpha=0.3)

# Add annotations
for i in [3, 6, 12]:
    if i in avg_ltv.index and not pd.isna(avg_ltv[i]):
        ax5.annotate(f'${avg_ltv[i]:.0f}',
                    xy=(i, avg_ltv[i]),
                    xytext=(i, avg_ltv[i] + 20),
                    fontsize=10, ha='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

plt.suptitle('NourishBox Cohort Analysis Dashboard',
             fontsize=18, fontweight='bold', y=0.995)

# Save the figure
output_path = 'data/nourishbox/cohort_analysis.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✓ Cohort analysis visualization saved to: {output_path}")

# ============================================================================
# KEY INSIGHTS
# ============================================================================
print("\n" + "="*70)
print("KEY COHORT INSIGHTS")
print("="*70)

# Month 1 retention
month1_retention = avg_retention[1] if 1 in avg_retention.index else 0
month3_retention = avg_retention[3] if 3 in avg_retention.index else 0
month6_retention = avg_retention[6] if 6 in avg_retention.index else 0
month12_retention = avg_retention[12] if 12 in avg_retention.index else 0

print(f"\n1. RETENTION RATES:")
print(f"   • Month 1:  {month1_retention:.1f}% of customers place a 2nd order")
print(f"   • Month 3:  {month3_retention:.1f}% retention (critical milestone)")
print(f"   • Month 6:  {month6_retention:.1f}% retention")
print(f"   • Month 12: {month12_retention:.1f}% retention")

# New Year vs Others
if 3 in retention_comparison.index:
    ny_month3 = retention_comparison.loc[3, 'New Year (Jan-Feb)']
    other_month3 = retention_comparison.loc[3, 'Other Months']
    print(f"\n2. NEW YEAR COHORT PERFORMANCE:")
    print(f"   • 3-month retention (New Year): {ny_month3:.1f}%")
    print(f"   • 3-month retention (Others):   {other_month3:.1f}%")
    print(f"   • Difference: {ny_month3 - other_month3:+.1f}% (New Year signups drop off faster)")

# LTV insights
ltv_3m = avg_ltv[3] if 3 in avg_ltv.index else 0
ltv_6m = avg_ltv[6] if 6 in avg_ltv.index else 0
ltv_12m = avg_ltv[12] if 12 in avg_ltv.index else 0

print(f"\n3. CUSTOMER LIFETIME VALUE:")
print(f"   • 3-month LTV:  ${ltv_3m:.2f}")
print(f"   • 6-month LTV:  ${ltv_6m:.2f}")
print(f"   • 12-month LTV: ${ltv_12m:.2f}")
print(f"   • Average monthly value: ${ltv_12m/12:.2f}")

# Best and worst cohorts
if len(retention_matrix_12m) > 0:
    cohort_month3 = retention_matrix_12m[3].dropna()
    if len(cohort_month3) > 0:
        best_cohort = cohort_month3.idxmax()
        worst_cohort = cohort_month3.idxmin()
        print(f"\n4. COHORT PERFORMANCE (3-month retention):")
        print(f"   • Best performing cohort:  {best_cohort} ({cohort_month3[best_cohort]:.1f}%)")
        print(f"   • Worst performing cohort: {worst_cohort} ({cohort_month3[worst_cohort]:.1f}%)")

print("\n" + "="*70)
print("Cohort analysis complete!")
print("="*70 + "\n")