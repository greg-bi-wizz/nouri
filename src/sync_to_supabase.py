"""
NourishBox Data Sync to Supabase
Syncs generated CSV data to Supabase PostgreSQL database

This script:
1. Reads CSV files from data/nourishbox/
2. Connects to your Supabase PostgreSQL database
3. Creates tables (if they don't exist)
4. Loads data into tables
5. Optionally: Clears old data and replaces with new data

Prerequisites:
    pip install psycopg2-binary python-dotenv

Usage:
    1. Create .env file with your Supabase credentials
    2. Run: python sync_to_supabase.py

Options:
    --clear     Clear all existing data before loading (fresh start)
    --append    Append new data to existing data (default)
    --update    Update existing records (based on primary keys)
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import pandas as pd
from dotenv import load_dotenv
import argparse
from pathlib import Path

# Load environment variables
load_dotenv()

# Configuration
DATA_DIR = 'data/nourishbox'
CSV_FILES = [
    'plan_dim.csv',
    'date_dim.csv',
    'customers.csv',
    'customer_preferences.csv',
    'subscriptions.csv',
    'subscription_monthly.csv',
    'orders.csv',
    'order_items.csv',
    'churn_events.csv',
    'reviews.csv',
    'marketing_campaigns.csv',
    'product_catalog.csv'
]

# Table configurations (table_name: primary_key)
TABLE_CONFIGS = {
    'plan_dim': 'plan_key',
    'date_dim': 'date_key',
    'customers': 'customer_id',
    'customer_preferences': 'customer_id',
    'subscriptions': 'subscription_id',
    'subscription_monthly': 'snapshot_id',
    'orders': 'order_id',
    'order_items': 'item_id',
    'churn_events': 'churn_id',
    'reviews': 'review_id',
    'marketing_campaigns': 'campaign_id',
    'product_catalog': 'product_id'
}


class SupabaseSync:
    """Handles syncing data to Supabase PostgreSQL database"""

    def __init__(self):
        """Initialize database connection from environment variables"""
        self.conn = None
        self.cursor = None

        # Get connection details from environment
        self.host = os.getenv('SUPABASE_HOST')
        self.database = os.getenv('SUPABASE_DB', 'postgres')
        self.user = os.getenv('SUPABASE_USER', 'postgres')
        self.password = os.getenv('SUPABASE_PASSWORD')
        self.port = os.getenv('SUPABASE_PORT', '5432')

        # Validate credentials
        if not all([self.host, self.password]):
            raise ValueError(
                "Missing Supabase credentials! Please set environment variables:\n"
                "  SUPABASE_HOST=db.xxxxx.supabase.co\n"
                "  SUPABASE_PASSWORD=your-password\n"
                "\nOr create a .env file with these values."
            )

    def connect(self):
        """Establish connection to Supabase"""
        try:
            print(f"\n🔌 Connecting to Supabase...")
            print(f"   Host: {self.host}")
            print(f"   Database: {self.database}")

            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode='require'  # Supabase requires SSL
            )
            self.cursor = self.conn.cursor()
            print("✅ Connected successfully!\n")

        except psycopg2.Error as e:
            print(f"\n❌ Connection failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Check your credentials in .env file")
            print("  2. Verify Supabase project is active")
            print("  3. Check if your IP is allowed (Supabase allows all by default)")
            sys.exit(1)

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\n✅ Disconnected from Supabase")

    def table_exists(self, table_name):
        """Check if table exists"""
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            );
        """
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone()[0]

    def create_table_from_csv(self, csv_file, table_name):
        """Create table schema based on CSV columns"""
        df = pd.read_csv(csv_file, nrows=5)  # Just read a few rows to get schema

        # Map pandas dtypes to PostgreSQL types
        type_mapping = {
            'int64': 'INTEGER',
            'float64': 'DECIMAL(14, 2)',
            'bool': 'BOOLEAN',
            'object': 'TEXT',
            'datetime64[ns]': 'DATE'
        }

        decimal_keywords = (
            'price', 'cost', 'total', 'value', 'budget', 'ctr', 'rate',
            'mrr', 'amount', 'discount'
        )
        date_columns = {'month_start', 'date'}

        # Build CREATE TABLE statement
        columns = []
        primary_key = TABLE_CONFIGS.get(table_name)

        for col, dtype in df.dtypes.items():
            name_lower = col.lower()
            pg_type = type_mapping.get(str(dtype), 'TEXT')

            if col == primary_key:
                columns.append(f'    {col} TEXT PRIMARY KEY')
            elif col in date_columns or name_lower.endswith('_date'):
                columns.append(f'    {col} DATE')
            elif name_lower.endswith('_id') and col != primary_key:
                columns.append(f'    {col} TEXT')
            elif name_lower in ['rating', 'age', 'household_size', 'quantity', 'calories',
                                'year', 'quarter', 'month', 'day', 'day_of_week']:
                columns.append(f'    {col} INTEGER')
            elif any(keyword in name_lower for keyword in decimal_keywords):
                columns.append(f'    {col} DECIMAL(14, 2)')
            elif str(dtype) == 'int64':
                columns.append(f'    {col} INTEGER')
            elif str(dtype) == 'float64':
                columns.append(f'    {col} DECIMAL(14, 2)')
            elif str(dtype) == 'bool':
                columns.append(f'    {col} BOOLEAN')
            else:
                columns.append(f'    {col} {pg_type}')

        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            {','.join(columns)}
            );
        """

        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print(f"   ✓ Table '{table_name}' ready")
        except psycopg2.Error as e:
            print(f"   ✗ Error creating table '{table_name}': {e}")
            self.conn.rollback()

    def clear_table(self, table_name):
        """Delete all data from table"""
        try:
            self.cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
            self.conn.commit()
            print(f"   ✓ Cleared existing data from '{table_name}'")
        except psycopg2.Error as e:
            print(f"   ✗ Error clearing table '{table_name}': {e}")
            self.conn.rollback()

    def get_row_count(self, table_name):
        """Get current row count in table"""
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            return self.cursor.fetchone()[0]
        except:
            return 0

    def load_csv_to_table(self, csv_file, table_name, mode='append'):
        """Load CSV data into PostgreSQL table"""
        print(f"\n📤 Loading {csv_file} → {table_name}")

        # Read CSV
        df = pd.read_csv(csv_file)

        # Convert NaN to None for PostgreSQL
        df = df.where(pd.notnull(df), None)

        # Convert boolean columns
        bool_cols = df.select_dtypes(include=['bool']).columns
        for col in bool_cols:
            df[col] = df[col].astype(object)  # Convert to object to handle None

        if len(df) == 0:
            print(f"   ⚠️  No data in {csv_file}, skipping...")
            return

        # Get current count
        current_count = self.get_row_count(table_name)

        # Prepare columns and values
        columns = df.columns.tolist()
        values = [tuple(row) for row in df.values]

        # Build INSERT statement
        insert_query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES %s
            ON CONFLICT ({}) DO NOTHING
        """).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.Identifier(TABLE_CONFIGS[table_name])
        )

        try:
            # Use execute_values for efficient bulk insert
            execute_values(
                self.cursor,
                insert_query.as_string(self.conn),
                values,
                page_size=1000
            )
            self.conn.commit()

            new_count = self.get_row_count(table_name)
            inserted = new_count - current_count

            print(f"   ✓ Loaded {len(df):,} rows")
            print(f"   ✓ Inserted: {inserted:,} new rows")
            print(f"   ✓ Total in table: {new_count:,} rows")

        except psycopg2.Error as e:
            print(f"   ✗ Error loading data: {e}")
            self.conn.rollback()

    def verify_data(self):
        """Verify data was loaded correctly"""
        print("\n" + "="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)

        total_rows = 0
        for table_name in TABLE_CONFIGS.keys():
            try:
                count = self.get_row_count(table_name)
                total_rows += count
                print(f"  {table_name:30s}: {count:>10,} rows")
            except:
                print(f"  {table_name:30s}: {'ERROR':>10s}")

        print("="*70)
        print(f"  {'TOTAL RECORDS':30s}: {total_rows:>10,}")
        print("="*70 + "\n")


def create_env_template():
    """Create .env template file if it doesn't exist"""
    env_file = Path('.env')

    if not env_file.exists():
        template = """# Supabase Connection Settings
# Get these from: Supabase Project → Settings → Database

# Your Supabase database host (without https://)
# Example: db.abcdefghijklmnop.supabase.co
SUPABASE_HOST=db.xxxxx.supabase.co

# Your database password (set when creating project)
SUPABASE_PASSWORD=your-password-here

# These are usually defaults (don't change unless you know what you're doing)
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PORT=5432
"""

        with open('.env', 'w') as f:
            f.write(template)

        print("\n📝 Created .env template file")
        print("   Please edit .env and add your Supabase credentials")
        print("\n   To get your credentials:")
        print("   1. Go to your Supabase project")
        print("   2. Settings → Database")
        print("   3. Copy 'Host' and 'Password'")
        print("   4. Paste into .env file\n")
        return True

    return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Sync NourishBox data to Supabase')
    parser.add_argument('--clear', action='store_true',
                       help='Clear existing data before loading (fresh start)')
    parser.add_argument('--setup', action='store_true',
                       help='Create .env template and setup instructions')
    args = parser.parse_args()

    # Setup mode
    if args.setup:
        create_env_template()
        return

    print("\n" + "="*70)
    print("NOURISHBOX → SUPABASE SYNC")
    print("="*70)

    # Check if CSV files exist
    if not os.path.exists(DATA_DIR):
        print(f"\n❌ Data directory not found: {DATA_DIR}")
        print("   Run 'python generate_nourishbox_data.py' first to generate data")
        sys.exit(1)

    # Check if .env exists
    if not Path('.env').exists():
        print("\n❌ .env file not found!")
        create_env_template()
        sys.exit(1)

    # Initialize sync
    sync = SupabaseSync()

    try:
        # Connect
        sync.connect()

        # Process each CSV file
        print("\n" + "="*70)
        print("CREATING TABLES")
        print("="*70)

        for csv_file in CSV_FILES:
            csv_path = os.path.join(DATA_DIR, csv_file)
            table_name = csv_file.replace('.csv', '')

            if not os.path.exists(csv_path):
                print(f"⚠️  Skipping {csv_file} (not found)")
                continue

            # Create table
            sync.create_table_from_csv(csv_path, table_name)

            # Clear if requested
            if args.clear:
                sync.clear_table(table_name)

        # Load data
        print("\n" + "="*70)
        print("LOADING DATA")
        print("="*70)

        for csv_file in CSV_FILES:
            csv_path = os.path.join(DATA_DIR, csv_file)
            table_name = csv_file.replace('.csv', '')

            if not os.path.exists(csv_path):
                continue

            sync.load_csv_to_table(csv_path, table_name)

        # Verify
        sync.verify_data()

        print("✅ Sync completed successfully!")
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("\n1. Connect Power BI:")
        print(f"   Server: {sync.host}")
        print(f"   Database: {sync.database}")
        print(f"   User: {sync.user}")
        print("\n2. Test in Supabase SQL Editor:")
        print("   SELECT COUNT(*) FROM customers;")
        print("   SELECT SUM(order_total) FROM orders;")
        print("\n3. Build your dashboards! 🎉\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    finally:
        sync.disconnect()


if __name__ == "__main__":
    main()
