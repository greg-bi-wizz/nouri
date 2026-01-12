"""
NourishBox - Example Analysis Script
Demonstrates basic exploratory data analysis on the generated data
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuration
DATA_DIR = 'data/nourishbox'

def load_data():
    """Load all datasets"""
    print("Loading datasets...")

    data = {
        'customers': pd.read_csv(f'{DATA_DIR}/customers.csv'),
        'preferences': pd.read_csv(f'{DATA_DIR}/customer_preferences.csv'),
        'subscriptions': pd.read_csv(f'{DATA_DIR}/subscriptions.csv'),
        'orders': pd.read_csv(f'{DATA_DIR}/orders.csv'),
        'order_items': pd.read_csv(f'{DATA_DIR}/order_items.csv'),
        'churn': pd.read_csv(f'{DATA_DIR}/churn_events.csv'),
        'reviews': pd.read_csv(f'{DATA_DIR}/reviews.csv'),
        'campaigns': pd.read_csv(f'{DATA_DIR}/marketing_campaigns.csv'),
        'products': pd.read_csv(f'{DATA_DIR}/product_catalog.csv')
    }

    print("✓ All datasets loaded successfully\n")
    return data

def basic_overview(data):
    """Print basic overview of the dataset"""
    print("="*70)
    print("DATASET OVERVIEW")
    print("="*70)

    for name, df in data.items():
        print(f"{name.upper():20s}: {len(df):,} rows × {len(df.columns)} columns")
    print()

def customer_analysis(data):
    """Analyze customer demographics and acquisition"""
    print("="*70)
    print("CUSTOMER ANALYSIS")
    print("="*70)

    customers = data['customers']

    # Age distribution
    print(f"\nAge Distribution:")
    print(f"  Average age: {customers['age'].mean():.1f} years")
    print(f"  Median age: {customers['age'].median():.0f} years")
    print(f"  Age range: {customers['age'].min()}-{customers['age'].max()}")

    # Gender distribution
    print(f"\nGender Distribution:")
    print(customers['gender'].value_counts())

    # Acquisition channels
    print(f"\nTop Acquisition Channels:")
    channel_counts = customers['acquisition_channel'].value_counts()
    for channel, count in channel_counts.head(5).items():
        pct = (count / len(customers)) * 100
        print(f"  {channel:20s}: {count:4d} ({pct:5.1f}%)")

    # Referrals
    referrals = customers['referred_by_customer_id'].notna().sum()
    print(f"\nReferral Program:")
    print(f"  Customers from referrals: {referrals} ({referrals/len(customers)*100:.1f}%)")
    print()

def subscription_analysis(data):
    """Analyze subscription patterns"""
    print("="*70)
    print("SUBSCRIPTION ANALYSIS")
    print("="*70)

    subscriptions = data['subscriptions']

    # Subscription plan distribution
    print(f"\nSubscription Plans (All Time):")
    plan_counts = subscriptions['plan_name'].value_counts()
    for plan, count in plan_counts.items():
        pct = (count / len(subscriptions)) * 100
        print(f"  {plan:25s}: {count:4d} ({pct:5.1f}%)")

    # Active vs Cancelled
    print(f"\nSubscription Status:")
    status_counts = subscriptions['status'].value_counts()
    for status, count in status_counts.items():
        pct = (count / len(subscriptions)) * 100
        print(f"  {status:15s}: {count:4d} ({pct:5.1f}%)")

    # Average subscription price
    print(f"\nPricing Metrics:")
    print(f"  Average monthly price: ${subscriptions['monthly_price'].mean():.2f}")
    print(f"  Median monthly price: ${subscriptions['monthly_price'].median():.2f}")
    print()

def revenue_analysis(data):
    """Analyze revenue metrics"""
    print("="*70)
    print("REVENUE ANALYSIS")
    print("="*70)

    orders = data['orders']

    # Convert date
    orders['order_date'] = pd.to_datetime(orders['order_date'])

    # Total revenue
    total_revenue = orders['order_total'].sum()
    print(f"\nTotal Revenue: ${total_revenue:,.2f}")

    # Average order value
    print(f"Average Order Value: ${orders['order_total'].mean():.2f}")

    # Monthly revenue trend
    monthly_revenue = orders.groupby(orders['order_date'].dt.to_period('M'))['order_total'].sum()
    print(f"\nRevenue by Month (Last 6 months):")
    for period, revenue in monthly_revenue.tail(6).items():
        print(f"  {period}: ${revenue:>10,.2f}")

    # Revenue by delivery status
    print(f"\nRevenue by Delivery Status:")
    for status in ['delivered', 'delayed', 'cancelled', 'pending']:
        rev = orders[orders['delivery_status'] == status]['order_total'].sum()
        pct = (rev / total_revenue) * 100
        print(f"  {status:15s}: ${rev:>12,.2f} ({pct:5.1f}%)")
    print()

def churn_analysis(data):
    """Analyze customer churn"""
    print("="*70)
    print("CHURN ANALYSIS")
    print("="*70)

    churn = data['churn']
    customers = data['customers']

    # Overall churn rate
    churn_rate = (len(churn) / len(customers)) * 100
    print(f"\nOverall Churn Rate: {churn_rate:.1f}%")

    # Average subscription length before churn
    avg_days = churn['subscription_length_days'].mean()
    print(f"Average Subscription Length (churned): {avg_days:.0f} days ({avg_days/30:.1f} months)")

    # Churn reasons
    print(f"\nTop Churn Reasons:")
    reason_counts = churn['churn_reason'].value_counts()
    for reason, count in reason_counts.head(7).items():
        pct = (count / len(churn)) * 100
        print(f"  {reason:25s}: {count:4d} ({pct:5.1f}%)")

    # Retention attempts
    retention_attempted = churn['attempted_retention'].sum()
    retention_success = churn['retention_offer_accepted'].sum()
    if retention_attempted > 0:
        success_rate = (retention_success / retention_attempted) * 100
        print(f"\nRetention Program:")
        print(f"  Retention attempts: {retention_attempted}")
        print(f"  Successful retentions: {retention_success}")
        print(f"  Success rate: {success_rate:.1f}%")
    print()

def review_analysis(data):
    """Analyze customer reviews"""
    print("="*70)
    print("REVIEW ANALYSIS")
    print("="*70)

    reviews = data['reviews']

    # Overall rating
    print(f"\nOverall Metrics:")
    print(f"  Total reviews: {len(reviews):,}")
    print(f"  Average rating: {reviews['rating'].mean():.2f}/5.0")
    print(f"  Median rating: {reviews['rating'].median():.0f}/5.0")

    # Rating distribution
    print(f"\nRating Distribution:")
    for rating in range(5, 0, -1):
        count = (reviews['rating'] == rating).sum()
        pct = (count / len(reviews)) * 100
        stars = '★' * rating + '☆' * (5 - rating)
        print(f"  {stars} ({rating}): {count:5d} ({pct:5.1f}%)")

    # Would recommend
    would_recommend = reviews['would_recommend'].sum()
    rec_pct = (would_recommend / len(reviews)) * 100
    print(f"\nWould Recommend: {would_recommend:,} ({rec_pct:.1f}%)")

    # Category ratings
    print(f"\nCategory Ratings (Average):")
    for category in ['meal_quality_rating', 'beauty_quality_rating', 'delivery_rating', 'value_rating']:
        avg = reviews[category].mean()
        print(f"  {category.replace('_', ' ').title():25s}: {avg:.2f}/5.0")
    print()

def marketing_analysis(data):
    """Analyze marketing campaign performance"""
    print("="*70)
    print("MARKETING CAMPAIGN ANALYSIS")
    print("="*70)

    campaigns = data['campaigns']

    # Total spend and conversions
    total_budget = campaigns['budget'].sum()
    total_conversions = campaigns['conversions'].sum()
    avg_cpa = total_budget / total_conversions if total_conversions > 0 else 0

    print(f"\nOverall Performance:")
    print(f"  Total campaigns: {len(campaigns)}")
    print(f"  Total budget: ${total_budget:,.2f}")
    print(f"  Total conversions: {total_conversions:,}")
    print(f"  Average CPA: ${avg_cpa:.2f}")

    # Best performing campaign types
    print(f"\nPerformance by Campaign Type:")
    campaign_perf = campaigns.groupby('campaign_type').agg({
        'budget': 'sum',
        'conversions': 'sum',
        'conversion_rate': 'mean',
        'cost_per_acquisition': 'mean'
    }).round(2)

    for camp_type, row in campaign_perf.iterrows():
        print(f"\n  {camp_type.upper()}:")
        print(f"    Budget: ${row['budget']:,.2f}")
        print(f"    Conversions: {row['conversions']:.0f}")
        print(f"    Avg Conversion Rate: {row['conversion_rate']:.2f}%")
        print(f"    Avg CPA: ${row['cost_per_acquisition']:.2f}")
    print()

def product_analysis(data):
    """Analyze product performance"""
    print("="*70)
    print("PRODUCT ANALYSIS")
    print("="*70)

    order_items = data['order_items']
    products = data['products']

    # Product type distribution
    print(f"\nProduct Type Distribution:")
    type_counts = order_items['product_type'].value_counts()
    for ptype, count in type_counts.items():
        pct = (count / len(order_items)) * 100
        print(f"  {ptype.title():15s}: {count:7,} ({pct:5.1f}%)")

    # Top products by volume
    print(f"\nTop 10 Products (by volume):")
    top_products = order_items['product_name'].value_counts().head(10)
    for i, (product, count) in enumerate(top_products.items(), 1):
        print(f"  {i:2d}. {product:40s}: {count:5,}")

    # Meal categories
    meal_items = order_items[order_items['product_type'] == 'meal']
    print(f"\nMeal Categories:")
    meal_cats = meal_items['product_category'].value_counts()
    for cat, count in meal_cats.items():
        pct = (count / len(meal_items)) * 100
        print(f"  {cat:15s}: {count:6,} ({pct:5.1f}%)")

    # Beauty categories
    beauty_items = order_items[order_items['product_type'] == 'beauty']
    print(f"\nBeauty Categories:")
    beauty_cats = beauty_items['product_category'].value_counts()
    for cat, count in beauty_cats.items():
        pct = (count / len(beauty_items)) * 100
        print(f"  {cat:20s}: {count:5,} ({pct:5.1f}%)")
    print()

def cohort_preview(data):
    """Preview cohort analysis opportunity"""
    print("="*70)
    print("COHORT ANALYSIS PREVIEW")
    print("="*70)

    customers = data['customers']
    subscriptions = data['subscriptions']

    # Convert dates
    customers['registration_date'] = pd.to_datetime(customers['registration_date'])
    customers['cohort'] = customers['registration_date'].dt.to_period('M')

    # Count by cohort
    cohort_sizes = customers.groupby('cohort').size()

    print(f"\nCustomer Cohorts (Monthly):")
    print(f"\nFirst 6 cohorts:")
    for period, count in cohort_sizes.head(6).items():
        print(f"  {period}: {count:4d} customers")

    print(f"\nLast 6 cohorts:")
    for period, count in cohort_sizes.tail(6).items():
        print(f"  {period}: {count:4d} customers")

    print(f"\nTotal cohorts: {len(cohort_sizes)}")
    print()

def main():
    """Run all analyses"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "NOURISHBOX DATA ANALYSIS" + " "*29 + "║")
    print("╚" + "="*68 + "╝")
    print()

    # Load data
    data = load_data()

    # Run analyses
    basic_overview(data)
    customer_analysis(data)
    subscription_analysis(data)
    revenue_analysis(data)
    churn_analysis(data)
    review_analysis(data)
    marketing_analysis(data)
    product_analysis(data)
    cohort_preview(data)

    print("="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nNext Steps:")
    print("  1. Load data into your BI tool (Tableau, Power BI, etc.)")
    print("  2. Create visualizations and dashboards")
    print("  3. Build predictive models for churn and CLV")
    print("  4. Perform cohort retention analysis")
    print("  5. Conduct A/B testing simulations")
    print("\nHappy analyzing!")
    print()

if __name__ == "__main__":
    main()
