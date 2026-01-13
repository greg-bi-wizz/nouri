"""
NourishBox Data Generator
Generate realistic synthetic data for a subscription box service offering healthy meals and beauty products.

Business Model:
- Three subscription plans: Meals Only, Beauty Only, Combo (Both)
- Monthly recurring subscriptions
- Customer preferences for dietary restrictions and beauty product types
- Churn analysis opportunities
- Cross-selling between meal and beauty products
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# Configuration
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2025, 12, 31)
NUM_CUSTOMERS = 4015
OUTPUT_DIR = 'data/nourishbox'

# Pricing assumptions for synthetic monetization
MEAL_PRICE_MARKUP = 1.8   # multiplier on meal unit cost
BEAUTY_PRICE_MARKUP = 1.0 # use provided retail_value directly

# Business constants
SUBSCRIPTION_PLANS = {
    'meal_basic': {'name': 'Meal Basic', 'price': 49.99, 'meals_per_week': 3, 'category': 'meals'},
    'meal_plus': {'name': 'Meal Plus', 'price': 79.99, 'meals_per_week': 5, 'category': 'meals'},
    'beauty_essentials': {'name': 'Beauty Essentials', 'price': 35.99, 'items_per_month': 4, 'category': 'beauty'},
    'beauty_premium': {'name': 'Beauty Premium', 'price': 59.99, 'items_per_month': 6, 'category': 'beauty'},
    'combo_starter': {'name': 'Combo Starter', 'price': 74.99, 'meals_per_week': 3, 'items_per_month': 3, 'category': 'combo'},
    'combo_deluxe': {'name': 'Combo Deluxe', 'price': 119.99, 'meals_per_week': 5, 'items_per_month': 6, 'category': 'combo'}
}

ACQUISITION_CHANNELS = ['organic_search', 'paid_social', 'referral', 'instagram', 'facebook_ads', 'google_ads', 'partnership', 'direct']
DIETARY_PREFERENCES = ['none', 'vegetarian', 'vegan', 'gluten_free', 'keto', 'paleo', 'dairy_free', 'low_carb']
BEAUTY_PREFERENCES = ['anti_aging', 'acne_treatment', 'hydration', 'natural_organic', 'fragrance_free', 'vegan_beauty', 'luxury']
SKIN_TYPES = ['normal', 'oily', 'dry', 'combination', 'sensitive']

MEAL_PRODUCTS = [
    # Protein-based meals
    {'name': 'Grilled Lemon Herb Chicken', 'category': 'protein', 'calories': 450, 'cost': 6.50, 'tags': ['gluten_free', 'dairy_free', 'high_protein']},
    {'name': 'Teriyaki Salmon Bowl', 'category': 'protein', 'calories': 520, 'cost': 8.00, 'tags': ['gluten_free', 'dairy_free', 'omega3']},
    {'name': 'Grass-Fed Beef Stir Fry', 'category': 'protein', 'calories': 480, 'cost': 7.50, 'tags': ['gluten_free', 'dairy_free', 'high_protein']},
    {'name': 'Turkey Meatballs Marinara', 'category': 'protein', 'calories': 410, 'cost': 6.00, 'tags': ['high_protein']},

    # Vegetarian meals
    {'name': 'Quinoa Buddha Bowl', 'category': 'vegetarian', 'calories': 380, 'cost': 5.50, 'tags': ['vegetarian', 'vegan', 'gluten_free', 'high_fiber']},
    {'name': 'Chickpea Tikka Masala', 'category': 'vegetarian', 'calories': 420, 'cost': 5.00, 'tags': ['vegetarian', 'vegan', 'gluten_free']},
    {'name': 'Spinach & Feta Stuffed Peppers', 'category': 'vegetarian', 'calories': 340, 'cost': 5.25, 'tags': ['vegetarian', 'gluten_free']},
    {'name': 'Black Bean Enchilada Bowl', 'category': 'vegetarian', 'calories': 390, 'cost': 4.75, 'tags': ['vegetarian', 'vegan', 'gluten_free']},

    # Keto/Low-carb
    {'name': 'Cauliflower Crust Pizza', 'category': 'low_carb', 'calories': 320, 'cost': 6.50, 'tags': ['keto', 'low_carb', 'gluten_free']},
    {'name': 'Zucchini Noodle Carbonara', 'category': 'low_carb', 'calories': 360, 'cost': 6.00, 'tags': ['keto', 'low_carb', 'gluten_free']},
    {'name': 'Avocado Chicken Salad', 'category': 'low_carb', 'calories': 400, 'cost': 7.00, 'tags': ['keto', 'low_carb', 'gluten_free', 'dairy_free']},

    # Paleo
    {'name': 'Paleo Shepherd\'s Pie', 'category': 'paleo', 'calories': 440, 'cost': 7.25, 'tags': ['paleo', 'gluten_free', 'dairy_free']},
    {'name': 'Sweet Potato & Bison Chili', 'category': 'paleo', 'calories': 390, 'cost': 7.50, 'tags': ['paleo', 'gluten_free', 'dairy_free']},

    # Vegan
    {'name': 'Lentil Curry Power Bowl', 'category': 'vegan', 'calories': 370, 'cost': 4.50, 'tags': ['vegan', 'vegetarian', 'gluten_free']},
    {'name': 'Tofu Pad Thai', 'category': 'vegan', 'calories': 420, 'cost': 5.50, 'tags': ['vegan', 'vegetarian']},
    {'name': 'Mediterranean Falafel Wrap', 'category': 'vegan', 'calories': 380, 'cost': 5.00, 'tags': ['vegan', 'vegetarian']},
]

BEAUTY_PRODUCTS = [
    # Skincare - Face
    {'name': 'Vitamin C Brightening Serum', 'category': 'skincare_face', 'cost': 18.00, 'retail_value': 45.00, 'tags': ['anti_aging', 'hydration']},
    {'name': 'Hyaluronic Acid Moisturizer', 'category': 'skincare_face', 'cost': 15.00, 'retail_value': 38.00, 'tags': ['hydration', 'fragrance_free']},
    {'name': 'Retinol Night Cream', 'category': 'skincare_face', 'cost': 22.00, 'retail_value': 55.00, 'tags': ['anti_aging', 'luxury']},
    {'name': 'Niacinamide Pore Refining Toner', 'category': 'skincare_face', 'cost': 12.00, 'retail_value': 28.00, 'tags': ['acne_treatment']},
    {'name': 'Gentle Foaming Cleanser', 'category': 'skincare_face', 'cost': 10.00, 'retail_value': 24.00, 'tags': ['fragrance_free', 'natural_organic']},
    {'name': 'Clay Detox Mask', 'category': 'skincare_face', 'cost': 14.00, 'retail_value': 32.00, 'tags': ['acne_treatment', 'natural_organic']},
    {'name': 'Rose Water Facial Mist', 'category': 'skincare_face', 'cost': 8.00, 'retail_value': 18.00, 'tags': ['hydration', 'natural_organic']},
    {'name': 'Peptide Eye Cream', 'category': 'skincare_face', 'cost': 20.00, 'retail_value': 48.00, 'tags': ['anti_aging', 'luxury']},

    # Skincare - Body
    {'name': 'Shea Butter Body Lotion', 'category': 'skincare_body', 'cost': 11.00, 'retail_value': 26.00, 'tags': ['hydration', 'natural_organic']},
    {'name': 'Coffee Scrub Exfoliator', 'category': 'skincare_body', 'cost': 13.00, 'retail_value': 30.00, 'tags': ['natural_organic']},
    {'name': 'Coconut Oil Body Butter', 'category': 'skincare_body', 'cost': 12.00, 'retail_value': 28.00, 'tags': ['hydration', 'vegan_beauty']},

    # Makeup
    {'name': 'Tinted Lip Balm SPF 15', 'category': 'makeup', 'cost': 7.00, 'retail_value': 16.00, 'tags': ['natural_organic']},
    {'name': 'Mineral Foundation Powder', 'category': 'makeup', 'cost': 16.00, 'retail_value': 38.00, 'tags': ['natural_organic', 'fragrance_free']},
    {'name': 'Lengthening Mascara', 'category': 'makeup', 'cost': 9.00, 'retail_value': 22.00, 'tags': ['vegan_beauty']},
    {'name': 'Cream Blush Stick', 'category': 'makeup', 'cost': 11.00, 'retail_value': 26.00, 'tags': ['natural_organic']},

    # Haircare
    {'name': 'Argan Oil Hair Mask', 'category': 'haircare', 'cost': 13.00, 'retail_value': 32.00, 'tags': ['hydration', 'natural_organic']},
    {'name': 'Volumizing Shampoo Bar', 'category': 'haircare', 'cost': 9.00, 'retail_value': 20.00, 'tags': ['natural_organic', 'vegan_beauty']},
    {'name': 'Leave-In Conditioner Spray', 'category': 'haircare', 'cost': 10.00, 'retail_value': 24.00, 'tags': ['hydration']},

    # Bath & Wellness
    {'name': 'Lavender Bath Salts', 'category': 'wellness', 'cost': 8.00, 'retail_value': 18.00, 'tags': ['natural_organic']},
    {'name': 'Green Tea Face Mask Sheet', 'category': 'wellness', 'cost': 3.50, 'retail_value': 8.00, 'tags': ['hydration', 'natural_organic']},
    {'name': 'Jade Facial Roller', 'category': 'wellness', 'cost': 12.00, 'retail_value': 28.00, 'tags': ['luxury', 'anti_aging']},
]

CHURN_REASONS = [
    'too_expensive', 'moving', 'product_quality', 'variety_lacking',
    'dietary_needs_changed', 'prefer_competitor', 'financial_reasons',
    'delivery_issues', 'too_much_food', 'lifestyle_change', 'other'
]

def create_output_directory():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ Output directory created: {OUTPUT_DIR}")

def get_seasonal_signup_multiplier(date):
    """
    Return signup multiplier based on seasonality:
    - January/February: HIGH (New Year's resolutions)
    - March-May: MEDIUM-HIGH (spring)
    - June-August: LOW (summer vacation)
    - September: MEDIUM (back to routine)
    - October: MEDIUM
    - November-December: LOW (holidays)
    """
    month = date.month
    multipliers = {
        1: 2.5,   # January - New Year's resolutions peak
        2: 2.0,   # February - still riding resolution wave
        3: 1.3,   # March - spring starts
        4: 1.2,   # April
        5: 1.1,   # May
        6: 0.6,   # June - summer slowdown
        7: 0.5,   # July - vacation season
        8: 0.6,   # August - end of summer
        9: 1.2,   # September - back to routine
        10: 1.0,  # October - normal
        11: 0.7,  # November - holidays approaching
        12: 0.6   # December - holiday season
    }
    return multipliers.get(month, 1.0)


def generate_plan_dimension():
    """Create a plan dimension from SUBSCRIPTION_PLANS"""
    plan_rows = []
    for plan_key, info in SUBSCRIPTION_PLANS.items():
        plan_rows.append({
            'plan_key': plan_key,
            'plan_name': info['name'],
            'category': info['category'],
            'monthly_price': info['price'],
            'meals_per_week': info.get('meals_per_week', -1),
            'items_per_month': info.get('items_per_month', -1)
        })
    return pd.DataFrame(plan_rows)


def generate_date_dimension(start_date, end_date):
    """Generate a simple date dimension for time intelligence"""
    rows = []
    current = start_date
    while current <= end_date:
        rows.append({
            'date_key': int(current.strftime('%Y%m%d')),
            'date': current.strftime('%Y-%m-%d'),
            'year': current.year,
            'quarter': (current.month - 1) // 3 + 1,
            'month': current.month,
            'day': current.day,
            'day_of_week': current.weekday() + 1,  # Monday=1
            'month_name': current.strftime('%B'),
            'year_month': current.strftime('%Y-%m'),
            'is_weekend': current.weekday() >= 5,
            'season': ('winter' if current.month in [12, 1, 2] else
                       'spring' if current.month in [3, 4, 5] else
                       'summer' if current.month in [6, 7, 8] else
                       'fall')
        })
        current += timedelta(days=1)
    return pd.DataFrame(rows)

def generate_customers(num_customers):
    """Generate customer data with demographics and acquisition info"""
    customers = []

    # Generate registration dates with seasonal patterns
    registration_dates = []
    current_date = START_DATE

    while len(registration_dates) < num_customers:
        # Get seasonal multiplier for current month
        multiplier = get_seasonal_signup_multiplier(current_date)

        # Base number of signups per day, adjusted by multiplier
        base_signups_per_day = (num_customers / (END_DATE - START_DATE).days)
        signups_this_day = int(base_signups_per_day * multiplier) + (1 if random.random() < (base_signups_per_day * multiplier) % 1 else 0)

        # Add some random variation (±30%)
        signups_this_day = max(0, int(signups_this_day * random.uniform(0.7, 1.3)))

        for _ in range(signups_this_day):
            if len(registration_dates) < num_customers:
                registration_dates.append(current_date)

        current_date += timedelta(days=1)
        if current_date > END_DATE:
            break

    # If we didn't generate enough dates, fill in the rest randomly
    while len(registration_dates) < num_customers:
        reg_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        registration_dates.append(reg_date)

    # Shuffle and trim to exact number
    random.shuffle(registration_dates)
    registration_dates = registration_dates[:num_customers]

    for i in range(num_customers):
        reg_date = registration_dates[i]

        customer = {
            'customer_id': f'CUST{str(i+1).zfill(6)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'registration_date': reg_date.strftime('%Y-%m-%d'),
            'acquisition_channel': random.choices(
                ACQUISITION_CHANNELS,
                weights=[15, 20, 18, 12, 15, 10, 7, 3],
                k=1
            )[0],
            'age': random.randint(22, 65),
            'gender': random.choice(['Female', 'Male', 'Non-binary', 'Prefer not to say']),
            'zip_code': fake.zipcode(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'referred_by_customer_id': None,  # Will populate later for referrals
            'is_new_year_signup': reg_date.month in [1, 2]  # Track New Year's resolution signups
        }
        customers.append(customer)

    df = pd.DataFrame(customers)

    # Add referrals for some customers who came via referral channel
    referral_customers = df[df['acquisition_channel'] == 'referral'].index
    potential_referrers = df[df.index < referral_customers.min()]['customer_id'].tolist() if len(referral_customers) > 0 else []

    for idx in referral_customers:
        if potential_referrers:
            df.at[idx, 'referred_by_customer_id'] = random.choice(potential_referrers)

    print(f"✓ Generated {len(df)} customers")
    print(f"  - New Year signups (Jan-Feb): {len(df[df['is_new_year_signup']])}")
    print(f"  - Summer signups (Jun-Aug): {len(df[df['registration_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').month in [6,7,8])])}")
    return df

def generate_customer_preferences(customers_df):
    """Generate customer preferences for dietary restrictions and beauty products"""
    preferences = []

    for _, customer in customers_df.iterrows():
        # Most customers have 0-2 dietary preferences
        num_dietary = random.choices([0, 1, 2], weights=[40, 45, 15], k=1)[0]
        dietary_prefs = random.sample(DIETARY_PREFERENCES[1:], num_dietary) if num_dietary > 0 else ['none']

        # Beauty preferences - 1-3 preferences
        num_beauty = random.choices([1, 2, 3], weights=[30, 50, 20], k=1)[0]
        beauty_prefs = random.sample(BEAUTY_PREFERENCES, num_beauty)

        pref = {
            'customer_id': customer['customer_id'],
            'dietary_preferences': ', '.join(dietary_prefs),
            'beauty_preferences': ', '.join(beauty_prefs),
            'skin_type': random.choice(SKIN_TYPES),
            'allergies': ', '.join(random.sample(['nuts', 'soy', 'shellfish', 'eggs', 'none'],
                                                k=random.choices([1, 2, 0], weights=[10, 5, 85], k=1)[0])) or 'none',
            'preferred_meal_time': random.choice(['lunch', 'dinner', 'both']),
            'household_size': random.choices([1, 2, 3, 4, 5], weights=[25, 35, 20, 15, 5], k=1)[0]
        }
        preferences.append(pref)

    df = pd.DataFrame(preferences)
    print(f"✓ Generated preferences for {len(df)} customers")
    return df

def generate_subscriptions(customers_df):
    """Generate subscription records for customers"""
    subscriptions = []
    subscription_id_counter = 1
    new_year_churns = 0

    for _, customer in customers_df.iterrows():
        reg_date = datetime.strptime(customer['registration_date'], '%Y-%m-%d')

        # Determine initial subscription plan based on customer profile
        age = customer['age']
        if age < 30:
            # Younger customers tend toward combo or beauty
            plan_weights = [10, 5, 15, 10, 25, 35]
        elif age < 45:
            # Middle age balanced
            plan_weights = [20, 20, 15, 15, 20, 10]
        else:
            # Older customers tend toward meals or premium
            plan_weights = [25, 25, 10, 20, 15, 5]

        current_plan = random.choices(list(SUBSCRIPTION_PLANS.keys()), weights=plan_weights, k=1)[0]
        start_date = reg_date

        # Determine if customer is still active or has churned
        days_since_reg = (END_DATE - reg_date).days

        # Special handling for New Year's resolution signups
        is_new_year_signup = customer['is_new_year_signup']

        if is_new_year_signup and days_since_reg >= 60:
            # 55% of New Year signups churn within 2-3 months
            if random.random() < 0.55:
                # Churn between 60-90 days (2-3 months)
                churn_days = random.randint(60, min(90, days_since_reg))
                end_date = start_date + timedelta(days=churn_days)
                status = 'cancelled'
                has_churned = True
                new_year_churns += 1
            else:
                # Those who survive the 3-month mark have normal churn
                if days_since_reg < 180:
                    churn_prob = 0.10
                elif days_since_reg < 365:
                    churn_prob = 0.20
                else:
                    churn_prob = 0.35

                has_churned = random.random() < churn_prob
                if has_churned:
                    churn_days = random.randint(120, min(days_since_reg, 730))
                    end_date = start_date + timedelta(days=churn_days)
                    status = 'cancelled'
                else:
                    end_date = None
                    status = 'active'
        else:
            # Normal churn probability for non-New Year signups
            if days_since_reg < 90:
                churn_prob = 0.05
            elif days_since_reg < 180:
                churn_prob = 0.15
            elif days_since_reg < 365:
                churn_prob = 0.25
            else:
                churn_prob = 0.40

            has_churned = random.random() < churn_prob

            if has_churned and days_since_reg >= 30:
                # Churned sometime between start and now (minimum 30 days)
                churn_days = random.randint(30, min(days_since_reg, 730))
                end_date = start_date + timedelta(days=churn_days)
                status = 'cancelled'
            else:
                end_date = None
                status = 'active'

        subscription = {
            'subscription_id': f'SUB{str(subscription_id_counter).zfill(6)}',
            'customer_id': customer['customer_id'],
            'plan_type': current_plan,
            'plan_name': SUBSCRIPTION_PLANS[current_plan]['name'],
            'monthly_price': SUBSCRIPTION_PLANS[current_plan]['price'],
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'status': status,
            'billing_cycle': 'monthly',
            'auto_renew': status == 'active' or random.random() > 0.3
        }
        subscriptions.append(subscription)
        subscription_id_counter += 1

        # Some customers upgrade/downgrade plans over time
        if not has_churned and days_since_reg > 180 and random.random() < 0.15:
            # Plan change
            plan_change_date = start_date + timedelta(days=random.randint(120, days_since_reg - 30))

            # Previous subscription ends
            subscriptions[-1]['end_date'] = plan_change_date.strftime('%Y-%m-%d')
            subscriptions[-1]['status'] = 'upgraded'

            # New subscription starts
            new_plan = random.choice([k for k in SUBSCRIPTION_PLANS.keys() if k != current_plan])
            subscription = {
                'subscription_id': f'SUB{str(subscription_id_counter).zfill(6)}',
                'customer_id': customer['customer_id'],
                'plan_type': new_plan,
                'plan_name': SUBSCRIPTION_PLANS[new_plan]['name'],
                'monthly_price': SUBSCRIPTION_PLANS[new_plan]['price'],
                'start_date': plan_change_date.strftime('%Y-%m-%d'),
                'end_date': None,
                'status': 'active',
                'billing_cycle': 'monthly',
                'auto_renew': True
            }
            subscriptions.append(subscription)
            subscription_id_counter += 1

    df = pd.DataFrame(subscriptions)
    print(f"✓ Generated {len(df)} subscription records")
    print(f"  - Active: {len(df[df['status'] == 'active'])}")
    print(f"  - Cancelled: {len(df[df['status'] == 'cancelled'])}")
    print(f"  - Upgraded: {len(df[df['status'] == 'upgraded'])}")
    print(f"  - New Year resolution churns (2-3 months): {new_year_churns}")
    return df


def generate_subscription_monthly(subscriptions_df):
    """Create a monthly subscription snapshot for MRR-style metrics"""
    rows = []
    snapshot_id = 1

    for _, sub in subscriptions_df.iterrows():
        start = datetime.strptime(sub['start_date'], '%Y-%m-%d').replace(day=1)
        sub_end = datetime.strptime(sub['end_date'], '%Y-%m-%d') if sub['end_date'] else END_DATE
        cursor = start

        while cursor <= sub_end and cursor <= END_DATE:
            status_at_month_start = sub['status']
            if sub['status'] == 'cancelled' and cursor > sub_end:
                break
            if sub['status'] == 'upgraded' and cursor >= sub_end:
                # upgraded subscriptions stop at the upgrade month boundary
                break

            rows.append({
                'snapshot_id': f'SNAP{str(snapshot_id).zfill(7)}',
                'subscription_id': sub['subscription_id'],
                'customer_id': sub['customer_id'],
                'plan_type': sub['plan_type'],
                'plan_name': sub['plan_name'],
                'month_start': cursor.strftime('%Y-%m-%d'),
                'status': status_at_month_start,
                'mrr': sub['monthly_price'] if status_at_month_start in ['active', 'upgraded'] else 0
            })
            snapshot_id += 1

            if cursor.month == 12:
                cursor = cursor.replace(year=cursor.year + 1, month=1, day=1)
            else:
                cursor = cursor.replace(month=cursor.month + 1, day=1)

    df = pd.DataFrame(rows)
    print(f"✓ Generated {len(df)} subscription monthly snapshots")
    return df

def get_seasonal_skip_probability(date):
    """
    Return probability of skipping order based on seasonality:
    - Summer months (Jun-Aug): Higher skip rate (vacations)
    - Holiday months (Nov-Dec): Higher skip rate (holiday eating)
    - Regular months: Lower skip rate
    """
    month = date.month
    skip_probs = {
        1: 0.05,   # January - normal
        2: 0.05,   # February - normal
        3: 0.05,   # March - normal
        4: 0.06,   # April - slightly higher (spring break)
        5: 0.06,   # May - slightly higher
        6: 0.12,   # June - vacation season starts
        7: 0.15,   # July - peak vacation
        8: 0.13,   # August - still vacation season
        9: 0.05,   # September - back to normal
        10: 0.05,  # October - normal
        11: 0.10,  # November - Thanksgiving
        12: 0.14   # December - holidays
    }
    return skip_probs.get(month, 0.05)

def generate_orders(subscriptions_df, campaigns_df):
    """Generate monthly order records for active subscription periods"""
    orders = []
    order_id_counter = 1
    total_skipped = 0
    seasonal_skips = {'summer': 0, 'holidays': 0, 'regular': 0}

    for _, subscription in subscriptions_df.iterrows():
        start = datetime.strptime(subscription['start_date'], '%Y-%m-%d')
        end = datetime.strptime(subscription['end_date'], '%Y-%m-%d') if subscription['end_date'] else END_DATE

        # Generate orders for each month of active subscription
        current_date = start
        while current_date <= end and current_date <= END_DATE:
            # Seasonal skip probability
            skip_prob = get_seasonal_skip_probability(current_date)

            if random.random() > skip_prob:
                # Order typically placed at start of month, delivered 2-5 days later
                order_date = current_date
                delivery_date = order_date + timedelta(days=random.randint(2, 5))

                # Delivery status
                if delivery_date <= END_DATE:
                    delivery_status = random.choices(
                        ['delivered', 'delayed', 'cancelled'],
                        weights=[94, 4, 2],
                        k=1
                    )[0]
                else:
                    delivery_status = 'pending'

                discount_amount = round(random.uniform(0, 15), 2) if random.random() < 0.15 else 0.00
                shipping_cost = 0.00 if subscription['monthly_price'] > 50 else 5.99
                order_total = max(0, subscription['monthly_price'] - discount_amount + shipping_cost)

                # Occasional campaign attribution
                campaign_id = None
                if len(campaigns_df) > 0 and random.random() < 0.35:
                    campaign_id = campaigns_df.sample(1).iloc[0]['campaign_id']

                order = {
                    'order_id': f'ORD{str(order_id_counter).zfill(7)}',
                    'subscription_id': subscription['subscription_id'],
                    'customer_id': subscription['customer_id'],
                    'order_date': order_date.strftime('%Y-%m-%d'),
                    'delivery_date': delivery_date.strftime('%Y-%m-%d') if delivery_status != 'cancelled' else None,
                    'order_total': order_total,
                    'delivery_status': delivery_status,
                    'delivery_address_zip': None,  # Would be linked to customer in real system
                    'shipping_cost': shipping_cost,
                    'discount_applied': discount_amount,
                    'plan_type_at_order': subscription['plan_type'],
                    'plan_price_at_order': subscription['monthly_price'],
                    'campaign_id': campaign_id,
                    'order_date_key': int(order_date.strftime('%Y%m%d')),
                    'year_month': order_date.strftime('%Y-%m')
                }
                orders.append(order)
                order_id_counter += 1
            else:
                # Order skipped (paused)
                total_skipped += 1
                if current_date.month in [6, 7, 8]:
                    seasonal_skips['summer'] += 1
                elif current_date.month in [11, 12]:
                    seasonal_skips['holidays'] += 1
                else:
                    seasonal_skips['regular'] += 1

            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)

    df = pd.DataFrame(orders)
    print(f"✓ Generated {len(df)} orders ({total_skipped} skipped)")
    print(f"  - Delivered: {len(df[df['delivery_status'] == 'delivered'])}")
    print(f"  - Delayed: {len(df[df['delivery_status'] == 'delayed'])}")
    print(f"  - Cancelled: {len(df[df['delivery_status'] == 'cancelled'])}")
    print(f"  - Pending: {len(df[df['delivery_status'] == 'pending'])}")
    print(f"  - Skipped (summer): {seasonal_skips['summer']}")
    print(f"  - Skipped (holidays): {seasonal_skips['holidays']}")
    print(f"  - Skipped (regular): {seasonal_skips['regular']}")
    return df

def generate_order_items(orders_df, subscriptions_df, preferences_df, products_df):
    """Generate individual product items for each order"""
    order_items = []
    item_id_counter = 1

    # Convert products_df to lists of dicts for easier filtering/sampling
    all_products = products_df.to_dict('records')
    meal_products = [p for p in all_products if p['product_type'] == 'meal']
    beauty_products = [p for p in all_products if p['product_type'] == 'beauty']

    # Create lookup dictionaries
    sub_to_plan = subscriptions_df.set_index('subscription_id')['plan_type'].to_dict()
    cust_to_prefs = preferences_df.set_index('customer_id')['dietary_preferences'].to_dict()

    for _, order in orders_df.iterrows():
        plan_type = sub_to_plan.get(order['subscription_id'])
        if not plan_type:
            continue

        plan_info = SUBSCRIPTION_PLANS[plan_type]
        plan_category = plan_info['category']

        # Get customer dietary preferences
        dietary_prefs = cust_to_prefs.get(order['customer_id'], 'none').split(', ')

        selected_items = []

        # Generate meal items
        if plan_category in ['meals', 'combo']:
            num_meals = plan_info.get('meals_per_week', 0) * 4  # 4 weeks per month

            # Filter meals based on dietary preferences
            available_meals = meal_products.copy()
            if 'none' not in dietary_prefs:
                available_meals = [
                    m for m in meal_products
                    if any(pref in m['tags'] for pref in dietary_prefs)
                ]

            if not available_meals:
                available_meals = meal_products

            # Select meals
            selected_meals = random.choices(available_meals, k=num_meals)

            for meal in selected_meals:
                selected_items.append({
                    'product_id': meal['product_id'],
                    'product_type': 'meal',
                    'product_name': meal['product_name'],
                    'product_category': meal['category'],
                    'quantity': 1,
                    'unit_cost': meal['cost_to_company'],
                    'calories': meal['calories'],
                    'retail_value': None,
                    'tags': meal['tags']
                })

        # Generate beauty items
        if plan_category in ['beauty', 'combo']:
            num_beauty = plan_info.get('items_per_month', 0)

            # Select variety of beauty products
            selected_beauty = random.sample(beauty_products, min(num_beauty, len(beauty_products)))

            for beauty in selected_beauty:
                selected_items.append({
                    'product_id': beauty['product_id'],
                    'product_type': 'beauty',
                    'product_name': beauty['product_name'],
                    'product_category': beauty['category'],
                    'quantity': 1,
                    'unit_cost': beauty['cost_to_company'],
                    'calories': -1,  # No calories for beauty products
                    'retail_value': beauty['retail_value'],
                    'tags': beauty['tags']
                })

        # Allocate discounts equally across items
        discount_per_item = 0.0
        if selected_items:
            discount_per_item = round(order['discount_applied'] / len(selected_items), 2) if order['discount_applied'] else 0.0

        for item in selected_items:
            if item['product_type'] == 'meal':
                line_price = round(item['unit_cost'] * MEAL_PRICE_MARKUP, 2)
            else:
                line_price = round(item['retail_value'], 2) if item['retail_value'] else round(item['unit_cost'] * (1 + BEAUTY_PRICE_MARKUP), 2)

            order_items.append({
                'item_id': f'ITEM{str(item_id_counter).zfill(8)}',
                'order_id': order['order_id'],
                'product_id': item['product_id'],
                'product_type': item['product_type'],
                'product_name': item['product_name'],
                'product_category': item['product_category'],
                'quantity': item['quantity'],
                'unit_cost': item['unit_cost'],
                'line_price': line_price,
                'line_discount': discount_per_item,
                'calories': item['calories'],
                'retail_value': item['retail_value'],
                'tags': item['tags']
            })
            item_id_counter += 1

    df = pd.DataFrame(order_items)
    print(f"✓ Generated {len(df)} order line items")
    print(f"  - Meal items: {len(df[df['product_type'] == 'meal'])}")
    print(f"  - Beauty items: {len(df[df['product_type'] == 'beauty'])}")
    return df

def generate_churn_events(subscriptions_df):
    """Generate churn event details for cancelled subscriptions"""
    churn_events = []

    cancelled_subs = subscriptions_df[subscriptions_df['status'] == 'cancelled']

    for _, sub in cancelled_subs.iterrows():
        event = {
            'churn_id': f'CHURN{str(len(churn_events) + 1).zfill(6)}',
            'subscription_id': sub['subscription_id'],
            'customer_id': sub['customer_id'],
            'churn_date': sub['end_date'],
            'subscription_length_days': (datetime.strptime(sub['end_date'], '%Y-%m-%d') -
                                        datetime.strptime(sub['start_date'], '%Y-%m-%d')).days,
            'churn_reason': random.choice(CHURN_REASONS),
            'attempted_retention': random.choice([True, False]),
            'retention_offer_accepted': False,
            'feedback_provided': random.choice([True, False]),
            'feedback_text': fake.sentence() if random.random() > 0.5 else None
        }

        if event['attempted_retention']:
            event['retention_offer_accepted'] = random.random() < 0.15  # 15% retention success

        churn_events.append(event)

    df = pd.DataFrame(churn_events)
    print(f"✓ Generated {len(df)} churn events")
    return df

def generate_reviews(orders_df, subscriptions_df):
    """Generate customer reviews for delivered orders"""
    reviews = []
    review_id_counter = 1

    # Reviews only for delivered orders
    delivered_orders = orders_df[orders_df['delivery_status'] == 'delivered'].copy()

    # About 40% of delivered orders get reviews
    reviewed_orders = delivered_orders.sample(n=int(len(delivered_orders) * 0.4))

    for _, order in reviewed_orders.iterrows():
        review_date = datetime.strptime(order['delivery_date'], '%Y-%m-%d') + timedelta(days=random.randint(1, 10))

        # Rating distribution - mostly positive with some negative
        rating = random.choices([1, 2, 3, 4, 5], weights=[3, 5, 12, 35, 45], k=1)[0]

        review = {
            'review_id': f'REV{str(review_id_counter).zfill(7)}',
            'order_id': order['order_id'],
            'customer_id': order['customer_id'],
            'subscription_id': order['subscription_id'],
            'review_date': review_date.strftime('%Y-%m-%d'),
            'rating': rating,
            'review_title': fake.sentence(nb_words=6).replace('.', ''),
            'review_text': fake.paragraph(nb_sentences=random.randint(2, 4)) if random.random() > 0.3 else None,
            'would_recommend': rating >= 4,
            'meal_quality_rating': random.randint(max(1, rating - 1), min(5, rating + 1)) if rating > 0 else None,
            'beauty_quality_rating': random.randint(max(1, rating - 1), min(5, rating + 1)) if rating > 0 else None,
            'delivery_rating': random.randint(max(1, rating - 1), min(5, rating + 1)) if rating > 0 else None,
            'value_rating': random.randint(max(1, rating - 1), min(5, rating + 1)) if rating > 0 else None
        }
        reviews.append(review)
        review_id_counter += 1

    df = pd.DataFrame(reviews)
    print(f"✓ Generated {len(df)} customer reviews")
    print(f"  - Average rating: {df['rating'].mean():.2f}")
    return df

def generate_marketing_campaigns():
    """Generate marketing campaign data"""
    campaigns = []

    campaign_types = ['email', 'social_media', 'influencer', 'paid_ads', 'referral_bonus', 'partnership']

    # Generate campaigns throughout the period
    current_date = START_DATE
    campaign_id = 1

    while current_date <= END_DATE:
        # 1-3 campaigns per month
        num_campaigns = random.randint(1, 3)

        for _ in range(num_campaigns):
            campaign_type = random.choice(campaign_types)
            start = current_date + timedelta(days=random.randint(0, 28))
            duration = random.randint(7, 30)
            end = start + timedelta(days=duration)

            if end > END_DATE:
                end = END_DATE

            budget = random.uniform(500, 10000)

            campaign = {
                'campaign_id': f'CAMP{str(campaign_id).zfill(5)}',
                'campaign_name': f'{campaign_type.title()} - {start.strftime("%b %Y")}',
                'campaign_type': campaign_type,
                'start_date': start.strftime('%Y-%m-%d'),
                'end_date': end.strftime('%Y-%m-%d'),
                'budget': round(budget, 2),
                'target_audience': random.choice(['new_customers', 'existing_customers', 'churned_customers', 'all']),
                'offer_type': random.choice(['discount_percent', 'discount_fixed', 'free_trial', 'free_gift', 'none']),
                'offer_value': random.choice([10, 15, 20, 25, 30, 50]) if random.random() > 0.3 else 0,
                'impressions': random.randint(10000, 500000),
                'clicks': random.randint(100, 20000),
                'conversions': random.randint(10, 500)
            }

            # Calculate CTR and conversion rate
            campaign['ctr'] = round((campaign['clicks'] / campaign['impressions']) * 100, 2)
            campaign['conversion_rate'] = round((campaign['conversions'] / campaign['clicks']) * 100, 2) if campaign['clicks'] > 0 else 0
            campaign['cost_per_acquisition'] = round(campaign['budget'] / campaign['conversions'], 2) if campaign['conversions'] > 0 else 0

            campaigns.append(campaign)
            campaign_id += 1

        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    df = pd.DataFrame(campaigns)
    print(f"✓ Generated {len(df)} marketing campaigns")
    return df

def generate_product_catalog():
    """Generate product catalog with all available products"""
    products = []
    product_id = 1

    # Meal products
    for meal in MEAL_PRODUCTS:
        product = {
            'product_id': f'PROD{str(product_id).zfill(5)}',
            'product_type': 'meal',
            'product_name': meal['name'],
            'category': meal['category'],
            'cost_to_company': meal['cost'],
            'calories': meal['calories'],
            'tags': ', '.join(meal['tags']),
            'active': random.choice([True, True, True, False]),  # 75% active
            'retail_value': round(meal['cost'] * MEAL_PRICE_MARKUP, 2)
        }
        products.append(product)
        product_id += 1

    # Beauty products
    for beauty in BEAUTY_PRODUCTS:
        product = {
            'product_id': f'PROD{str(product_id).zfill(5)}',
            'product_type': 'beauty',
            'product_name': beauty['name'],
            'category': beauty['category'],
            'cost_to_company': beauty['cost'],
            'calories': -1,  # No calories for beauty products
            'retail_value': beauty['retail_value'],
            'tags': ', '.join(beauty['tags']),
            'active': random.choice([True, True, True, False])
        }
        products.append(product)
        product_id += 1

    df = pd.DataFrame(products)
    print(f"✓ Generated product catalog with {len(df)} products")
    return df

def generate_all_data():
    """Main function to generate all datasets"""
    print("\n" + "="*60)
    print("NourishBox Data Generation Started")
    print("="*60 + "\n")

    create_output_directory()

    # Generate all datasets
    print("\n[1/13] Generating customers...")
    customers_df = generate_customers(NUM_CUSTOMERS)

    print("\n[2/13] Generating customer preferences...")
    preferences_df = generate_customer_preferences(customers_df)

    print("\n[3/13] Generating subscriptions...")
    subscriptions_df = generate_subscriptions(customers_df)

    print("\n[4/13] Generating marketing campaigns...")
    campaigns_df = generate_marketing_campaigns()

    print("\n[5/13] Generating orders...")
    orders_df = generate_orders(subscriptions_df, campaigns_df)

    print("\n[6/13] Generating product catalog...")
    products_df = generate_product_catalog()

    print("\n[7/13] Generating order items...")
    order_items_df = generate_order_items(orders_df, subscriptions_df, preferences_df, products_df)

    print("\n[8/13] Generating churn events...")
    churn_df = generate_churn_events(subscriptions_df)

    print("\n[9/13] Generating reviews...")
    reviews_df = generate_reviews(orders_df, subscriptions_df)

    print("\n[10/13] Generating plan dimension...")
    plan_dim_df = generate_plan_dimension()

    print("\n[11/13] Generating date dimension...")
    date_dim_df = generate_date_dimension(START_DATE, END_DATE)

    print("\n[12/13] Generating subscription monthly snapshots...")
    subscription_monthly_df = generate_subscription_monthly(subscriptions_df)


    # Save all datasets
    print("\n[13/13] Saving datasets to CSV files...")
    customers_df.to_csv(f'{OUTPUT_DIR}/customers.csv', index=False)
    preferences_df.to_csv(f'{OUTPUT_DIR}/customer_preferences.csv', index=False)
    subscriptions_df.to_csv(f'{OUTPUT_DIR}/subscriptions.csv', index=False)
    orders_df.to_csv(f'{OUTPUT_DIR}/orders.csv', index=False)
    order_items_df.to_csv(f'{OUTPUT_DIR}/order_items.csv', index=False)
    churn_df.to_csv(f'{OUTPUT_DIR}/churn_events.csv', index=False)
    reviews_df.to_csv(f'{OUTPUT_DIR}/reviews.csv', index=False)
    campaigns_df.to_csv(f'{OUTPUT_DIR}/marketing_campaigns.csv', index=False)
    products_df.to_csv(f'{OUTPUT_DIR}/product_catalog.csv', index=False)
    plan_dim_df.to_csv(f'{OUTPUT_DIR}/plan_dim.csv', index=False)
    date_dim_df.to_csv(f'{OUTPUT_DIR}/date_dim.csv', index=False)
    subscription_monthly_df.to_csv(f'{OUTPUT_DIR}/subscription_monthly.csv', index=False)

    print("\n" + "="*60)
    print("✅ Data Generation Complete!")
    print("="*60)
    print(f"\nOutput location: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    print(f"  1. customers.csv ({len(customers_df)} rows)")
    print(f"  2. customer_preferences.csv ({len(preferences_df)} rows)")
    print(f"  3. subscriptions.csv ({len(subscriptions_df)} rows)")
    print(f"  4. orders.csv ({len(orders_df)} rows)")
    print(f"  5. order_items.csv ({len(order_items_df)} rows)")
    print(f"  6. churn_events.csv ({len(churn_df)} rows)")
    print(f"  7. reviews.csv ({len(reviews_df)} rows)")
    print(f"  8. marketing_campaigns.csv ({len(campaigns_df)} rows)")
    print(f"  9. product_catalog.csv ({len(products_df)} rows)")
    print(f" 10. plan_dim.csv ({len(plan_dim_df)} rows)")
    print(f" 11. date_dim.csv ({len(date_dim_df)} rows)")
    print(f" 12. subscription_monthly.csv ({len(subscription_monthly_df)} rows)")

    # Summary statistics
    print("\n" + "="*60)
    print("Business Metrics Summary")
    print("="*60)
    print(f"Total Customers: {len(customers_df)}")
    print(f"Active Subscriptions: {len(subscriptions_df[subscriptions_df['status'] == 'active'])}")
    print(f"Churned Customers: {len(churn_df)}")
    print(f"Churn Rate: {(len(churn_df) / len(customers_df) * 100):.1f}%")
    print(f"Total Orders: {len(orders_df)}")
    print(f"Total Revenue: ${orders_df['order_total'].sum():,.2f}")
    print(f"Average Order Value: ${orders_df['order_total'].mean():.2f}")
    print(f"Average Review Rating: {reviews_df['rating'].mean():.2f}/5.0")
    print(f"Review Response Rate: {(len(reviews_df) / len(orders_df[orders_df['delivery_status'] == 'delivered']) * 100):.1f}%")
    print("="*60 + "\n")

if __name__ == "__main__":
    generate_all_data()
