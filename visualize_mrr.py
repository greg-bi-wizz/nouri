"""
NourishBox MRR Visualization
Visualize Monthly Recurring Revenue over time
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Configuration
DATA_DIR = 'data/nourishbox'

def calculate_mrr():
    """Calculate Monthly Recurring Revenue from subscriptions and orders"""

    print("Loading data...")

    # Load subscriptions
    subscriptions = pd.read_csv(f'{DATA_DIR}/subscriptions.csv')
    orders = pd.read_csv(f'{DATA_DIR}/orders.csv')

    # Convert dates
    subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
    subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'])
    orders['order_date'] = pd.to_datetime(orders['order_date'])

    print(f"✓ Loaded {len(subscriptions)} subscriptions")
    print(f"✓ Loaded {len(orders)} orders\n")

    # Get date range
    start_date = subscriptions['start_date'].min()
    end_date = datetime(2024, 12, 31)

    # Create monthly date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')

    mrr_data = []

    print("Calculating MRR for each month...")

    for current_date in date_range:
        # Count active subscriptions for this month
        active_subs = subscriptions[
            (subscriptions['start_date'] <= current_date) &
            ((subscriptions['end_date'].isna()) | (subscriptions['end_date'] >= current_date))
        ]

        # Calculate MRR (sum of monthly prices for active subscriptions)
        mrr = active_subs['monthly_price'].sum()

        # Count active subscribers
        active_count = len(active_subs)

        # Calculate actual revenue for the month (from orders)
        month_start = current_date
        month_end = current_date + pd.DateOffset(months=1)

        actual_revenue = orders[
            (orders['order_date'] >= month_start) &
            (orders['order_date'] < month_end) &
            (orders['delivery_status'].isin(['delivered', 'pending', 'delayed']))
        ]['order_total'].sum()

        mrr_data.append({
            'date': current_date,
            'mrr': mrr,
            'active_subscribers': active_count,
            'actual_revenue': actual_revenue,
            'year_month': current_date.strftime('%Y-%m')
        })

    mrr_df = pd.DataFrame(mrr_data)

    print(f"✓ Calculated MRR for {len(mrr_df)} months\n")

    return mrr_df


def create_mrr_visualization(mrr_df):
    """Create comprehensive MRR visualizations"""

    print("Creating visualizations...")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('NourishBox - Monthly Recurring Revenue Analysis',
                 fontsize=16, fontweight='bold', y=0.995)

    # Color scheme
    primary_color = '#2E86AB'    # Blue
    secondary_color = '#A23B72'  # Purple
    success_color = '#06A77D'    # Green

    # ========================================================================
    # Plot 1: MRR Over Time (Main Chart)
    # ========================================================================
    ax1 = axes[0, 0]
    ax1.plot(mrr_df['date'], mrr_df['mrr'],
             linewidth=3, color=primary_color, marker='o', markersize=4)
    ax1.fill_between(mrr_df['date'], mrr_df['mrr'],
                      alpha=0.3, color=primary_color)

    # Format
    ax1.set_title('Monthly Recurring Revenue (MRR)',
                  fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Date', fontsize=10)
    ax1.set_ylabel('MRR ($)', fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Date formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add current MRR annotation
    current_mrr = mrr_df['mrr'].iloc[-1]
    ax1.annotate(f'Current MRR:\n${current_mrr:,.0f}',
                xy=(mrr_df['date'].iloc[-1], current_mrr),
                xytext=(-100, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=primary_color, alpha=0.8),
                color='white', fontweight='bold', fontsize=10,
                arrowprops=dict(arrowstyle='->', color=primary_color, lw=2))

    # ========================================================================
    # Plot 2: Active Subscribers Over Time
    # ========================================================================
    ax2 = axes[0, 1]
    ax2.plot(mrr_df['date'], mrr_df['active_subscribers'],
             linewidth=3, color=secondary_color, marker='s', markersize=4)
    ax2.fill_between(mrr_df['date'], mrr_df['active_subscribers'],
                      alpha=0.3, color=secondary_color)

    ax2.set_title('Active Subscribers Over Time',
                  fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Date', fontsize=10)
    ax2.set_ylabel('Active Subscribers', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add current subscriber annotation
    current_subs = mrr_df['active_subscribers'].iloc[-1]
    ax2.annotate(f'{current_subs:,} subscribers',
                xy=(mrr_df['date'].iloc[-1], current_subs),
                xytext=(-100, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=secondary_color, alpha=0.8),
                color='white', fontweight='bold', fontsize=10,
                arrowprops=dict(arrowstyle='->', color=secondary_color, lw=2))

    # ========================================================================
    # Plot 3: MRR vs Actual Revenue
    # ========================================================================
    ax3 = axes[1, 0]

    x_pos = np.arange(len(mrr_df))
    width = 0.35

    ax3.bar(x_pos - width/2, mrr_df['mrr'], width,
            label='MRR (Expected)', color=primary_color, alpha=0.8)
    ax3.bar(x_pos + width/2, mrr_df['actual_revenue'], width,
            label='Actual Revenue', color=success_color, alpha=0.8)

    ax3.set_title('MRR vs Actual Revenue',
                  fontsize=12, fontweight='bold', pad=10)
    ax3.set_xlabel('Month', fontsize=10)
    ax3.set_ylabel('Revenue ($)', fontsize=10)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax3.legend(loc='upper left', fontsize=9)

    # Show every 6th month label
    tick_positions = range(0, len(mrr_df), 6)
    tick_labels = [mrr_df['year_month'].iloc[i] for i in tick_positions]
    ax3.set_xticks(tick_positions)
    ax3.set_xticklabels(tick_labels, rotation=45, ha='right')

    # ========================================================================
    # Plot 4: MRR Growth Rate (Month-over-Month)
    # ========================================================================
    ax4 = axes[1, 1]

    # Calculate month-over-month growth rate
    mrr_df['growth_rate'] = mrr_df['mrr'].pct_change() * 100

    # Color positive/negative growth differently
    colors = [success_color if x >= 0 else '#E63946' for x in mrr_df['growth_rate'][1:]]

    ax4.bar(mrr_df['date'][1:], mrr_df['growth_rate'][1:],
            color=colors, alpha=0.8, width=20)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

    ax4.set_title('MRR Growth Rate (Month-over-Month)',
                  fontsize=12, fontweight='bold', pad=10)
    ax4.set_xlabel('Date', fontsize=10)
    ax4.set_ylabel('Growth Rate (%)', fontsize=10)
    ax4.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))

    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add average growth rate
    avg_growth = mrr_df['growth_rate'][1:].mean()
    ax4.axhline(y=avg_growth, color='gray', linestyle='--', linewidth=1.5,
                label=f'Avg: {avg_growth:.2f}%')
    ax4.legend(loc='upper left', fontsize=9)

    # ========================================================================
    # Adjust layout and save
    # ========================================================================
    plt.tight_layout()

    # Save figure
    output_file = 'mrr_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved visualization: {output_file}")

    # Show plot
    plt.show()

    return mrr_df


def print_mrr_summary(mrr_df):
    """Print MRR summary statistics"""

    print("\n" + "="*70)
    print("MRR SUMMARY STATISTICS")
    print("="*70)

    # Current metrics
    current = mrr_df.iloc[-1]
    first = mrr_df.iloc[0]

    print(f"\n📊 Current Metrics (as of {current['year_month']}):")
    print(f"  MRR:                ${current['mrr']:,.2f}")
    print(f"  Active Subscribers: {current['active_subscribers']:,}")
    print(f"  ARPU (Avg Revenue Per User): ${current['mrr'] / current['active_subscribers']:.2f}")
    print(f"  ARR (Annual Run Rate): ${current['mrr'] * 12:,.2f}")

    # Growth metrics
    print(f"\n📈 Growth Metrics:")
    total_growth = ((current['mrr'] - first['mrr']) / first['mrr']) * 100
    print(f"  Total MRR Growth:   {total_growth:+.1f}%")
    print(f"  Starting MRR:       ${first['mrr']:,.2f} ({first['year_month']})")
    print(f"  Current MRR:        ${current['mrr']:,.2f} ({current['year_month']})")

    avg_monthly_growth = mrr_df['growth_rate'][1:].mean()
    print(f"  Avg Monthly Growth: {avg_monthly_growth:+.2f}%")

    # Peak metrics
    peak_mrr = mrr_df['mrr'].max()
    peak_date = mrr_df[mrr_df['mrr'] == peak_mrr]['year_month'].iloc[0]
    print(f"  Peak MRR:           ${peak_mrr:,.2f} ({peak_date})")

    # Subscriber metrics
    print(f"\n👥 Subscriber Metrics:")
    print(f"  Starting Subscribers: {first['active_subscribers']:,}")
    print(f"  Current Subscribers:  {current['active_subscribers']:,}")
    sub_growth = current['active_subscribers'] - first['active_subscribers']
    print(f"  Net Growth:           {sub_growth:+,} subscribers")

    # Revenue comparison
    print(f"\n💰 Revenue Comparison:")
    total_mrr = mrr_df['mrr'].sum()
    total_actual = mrr_df['actual_revenue'].sum()
    print(f"  Total Expected (MRR): ${total_mrr:,.2f}")
    print(f"  Total Actual Revenue: ${total_actual:,.2f}")
    print(f"  Revenue Realization:  {(total_actual / total_mrr * 100):.1f}%")

    # Monthly breakdown (last 12 months)
    print(f"\n📅 Last 12 Months MRR:")
    last_12 = mrr_df.tail(12)
    for _, row in last_12.iterrows():
        growth = row['growth_rate']
        growth_str = f"{growth:+.1f}%" if pd.notna(growth) else "N/A"
        print(f"  {row['year_month']}: ${row['mrr']:>10,.2f}  ({row['active_subscribers']:>4,} subs)  {growth_str:>8}")

    print("="*70 + "\n")


def main():
    """Main execution"""

    print("\n" + "="*70)
    print("NOURISHBOX MRR ANALYSIS")
    print("="*70 + "\n")

    # Calculate MRR
    mrr_df = calculate_mrr()

    # Create visualizations
    mrr_visualization = create_mrr_visualization(mrr_df)

    # Print summary
    print_mrr_summary(mrr_df)

    # Save MRR data to CSV for further analysis
    output_csv = 'mrr_data.csv'
    mrr_df.to_csv(output_csv, index=False)
    print(f"✓ MRR data saved to: {output_csv}")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nOutputs:")
    print(f"  1. mrr_analysis.png  - Visual charts")
    print(f"  2. mrr_data.csv      - Raw MRR data")
    print("\n")


if __name__ == "__main__":
    main()
