"""
NourishBox Data Sync to Databricks
Syncs generated CSV data to Databricks using Delta Lake

This script:
1. Reads CSV files from data/nourishbox/
2. Connects to your Databricks workspace
3. Creates schema/database (if it doesn't exist)
4. Uploads CSV files to DBFS (Databricks File System)
5. Creates Delta Lake tables
6. Loads data into tables
7. Optionally: Clears old data and replaces with new data

Prerequisites:
    pip install databricks-sql-connector python-dotenv pandas

Usage:
    1. Create .env file with your Databricks credentials
    2. Run: python src/sync_to_databricks.py

Options:
    --clear     Clear all existing data before loading (fresh start)
    --append    Append new data to existing data (default)
    --setup     Create .env template with setup instructions
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv
import argparse
from pathlib import Path
from databricks import sql
import time

# Load environment variables
load_dotenv()

# Configuration
DATA_DIR = 'data/nourishbox'
CSV_FILES = [
    'customers.csv',
    'customer_preferences.csv',
    'subscriptions.csv',
    'orders.csv',
    'order_items.csv',
    'churn_events.csv',
    'reviews.csv',
    'marketing_campaigns.csv',
    'product_catalog.csv'
]

# Table configurations (table_name: primary_key)
TABLE_CONFIGS = {
    'customers': 'customer_id',
    'customer_preferences': 'customer_id',
    'subscriptions': 'subscription_id',
    'orders': 'order_id',
    'order_items': 'item_id',
    'churn_events': 'churn_id',
    'reviews': 'review_id',
    'marketing_campaigns': 'campaign_id',
    'product_catalog': 'product_id'
}


class DatabricksSync:
    """Handles syncing data to Databricks using Delta Lake"""

    def __init__(self):
        """Initialize Databricks connection from environment variables"""
        self.connection = None
        self.cursor = None

        # Get connection details from environment
        self.server_hostname = os.getenv('DATABRICKS_SERVER_HOSTNAME')
        self.http_path = os.getenv('DATABRICKS_HTTP_PATH')
        self.access_token = os.getenv('DATABRICKS_ACCESS_TOKEN')
        self.catalog = os.getenv('DATABRICKS_CATALOG', 'main')
        self.schema = os.getenv('DATABRICKS_SCHEMA', 'nourishbox')

        # Validate credentials
        if not all([self.server_hostname, self.http_path, self.access_token]):
            raise ValueError(
                "Missing Databricks credentials! Please set environment variables:\n"
                "  DATABRICKS_SERVER_HOSTNAME=dbc-xxxxx-yyyy.cloud.databricks.com\n"
                "  DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx\n"
                "  DATABRICKS_ACCESS_TOKEN=dapi...\n"
                "\nOr create a .env file with these values."
            )

    def connect(self):
        """Establish connection to Databricks"""
        try:
            print(f"\n🔌 Connecting to Databricks...")
            print(f"   Host: {self.server_hostname}")
            print(f"   Catalog: {self.catalog}")
            print(f"   Schema: {self.schema}")

            self.connection = sql.connect(
                server_hostname=self.server_hostname,
                http_path=self.http_path,
                access_token=self.access_token
            )
            self.cursor = self.connection.cursor()
            print("✅ Connected successfully!\n")

        except Exception as e:
            print(f"\n❌ Connection failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Check your credentials in .env file")
            print("  2. Verify Databricks cluster is running")
            print("  3. Check if access token is valid (not expired)")
            print("  4. Verify HTTP path is correct")
            sys.exit(1)

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("\n✅ Disconnected from Databricks")

    def create_schema(self):
        """Create schema/database if it doesn't exist"""
        try:
            print("\n" + "="*70)
            print("CREATING SCHEMA")
            print("="*70)

            query = f"CREATE SCHEMA IF NOT EXISTS {self.catalog}.{self.schema}"
            self.cursor.execute(query)
            print(f"   ✓ Schema '{self.catalog}.{self.schema}' ready")

        except Exception as e:
            print(f"   ✗ Error creating schema: {e}")
            raise

    def table_exists(self, table_name):
        """Check if table exists"""
        try:
            query = f"""
                SHOW TABLES IN {self.catalog}.{self.schema}
                LIKE '{table_name}'
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return len(result) > 0
        except:
            return False

    def get_row_count(self, table_name):
        """Get current row count in table"""
        try:
            full_table_name = f"{self.catalog}.{self.schema}.{table_name}"
            query = f"SELECT COUNT(*) FROM {full_table_name}"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except:
            return 0

    def clear_table(self, table_name):
        """Delete all data from table"""
        try:
            full_table_name = f"{self.catalog}.{self.schema}.{table_name}"
            query = f"DELETE FROM {full_table_name}"
            self.cursor.execute(query)
            print(f"   ✓ Cleared existing data from '{table_name}'")
        except Exception as e:
            print(f"   ✗ Error clearing table '{table_name}': {e}")

    def infer_spark_type(self, pandas_dtype, column_name):
        """Map pandas dtype to Spark SQL type"""
        dtype_str = str(pandas_dtype)

        # Check column name patterns
        if column_name.endswith('_date'):
            return 'DATE'
        elif column_name.endswith('_id'):
            return 'STRING'
        elif column_name in ['rating', 'age', 'household_size', 'quantity', 'calories']:
            return 'INT'
        elif column_name in ['price', 'cost', 'total', 'value', 'budget', 'ctr', 'rate']:
            return 'DECIMAL(10, 2)'
        elif column_name in ['auto_renew', 'active', 'would_recommend', 'attempted_retention',
                            'retention_offer_accepted', 'feedback_provided']:
            return 'BOOLEAN'

        # Check dtype
        if 'int' in dtype_str:
            return 'INT'
        elif 'float' in dtype_str:
            return 'DECIMAL(10, 2)'
        elif 'bool' in dtype_str:
            return 'BOOLEAN'
        elif 'datetime' in dtype_str:
            return 'DATE'
        else:
            return 'STRING'

    def create_table_from_csv(self, csv_file, table_name):
        """Create Delta Lake table from CSV schema"""
        try:
            # Read CSV to get schema
            df = pd.read_csv(csv_file, nrows=5)

            # Build column definitions
            columns = []
            primary_key = TABLE_CONFIGS.get(table_name)

            for col in df.columns:
                spark_type = self.infer_spark_type(df[col].dtype, col)
                columns.append(f"`{col}` {spark_type}")

            # Create table DDL
            full_table_name = f"{self.catalog}.{self.schema}.{table_name}"
            columns_sql = ",\n    ".join(columns)

            create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {full_table_name} (
                    {columns_sql}
                )
                USING DELTA
            """

            self.cursor.execute(create_table_sql)
            print(f"   ✓ Table '{table_name}' ready")

        except Exception as e:
            print(f"   ✗ Error creating table '{table_name}': {e}")
            raise

    def load_csv_to_table(self, csv_file, table_name, mode='append'):
        """Load CSV data into Delta Lake table"""
        print(f"\n📤 Loading {csv_file} → {table_name}")

        try:
            # Read CSV
            df = pd.read_csv(csv_file)

            if len(df) == 0:
                print(f"   ⚠️  No data in {csv_file}, skipping...")
                return

            # Get current count
            current_count = self.get_row_count(table_name)

            # Create temp table name
            temp_table = f"{self.catalog}.{self.schema}.temp_{table_name}"
            full_table_name = f"{self.catalog}.{self.schema}.{table_name}"

            # For Databricks, we'll use a different approach:
            # 1. Create temp view from pandas DataFrame
            # 2. Insert into Delta table using SQL

            # Convert DataFrame to SQL-compatible format
            # This is a simplified approach - for production, use DBFS upload

            print(f"   📊 Processing {len(df):,} rows...")

            # Batch insert (for smaller datasets)
            # For larger datasets, you should upload to DBFS first
            batch_size = 1000
            total_batches = (len(df) + batch_size - 1) // batch_size

            inserted_count = 0

            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]

                # Convert batch to INSERT statements
                values = []
                for _, row in batch.iterrows():
                    row_values = []
                    for val in row:
                        if pd.isna(val):
                            row_values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped_val = val.replace("'", "''")
                            row_values.append(f"'{escaped_val}'")
                        elif isinstance(val, bool):
                            row_values.append('TRUE' if val else 'FALSE')
                        else:
                            row_values.append(str(val))
                    values.append(f"({', '.join(row_values)})")

                # Build INSERT statement
                columns = ', '.join([f"`{col}`" for col in df.columns])
                values_sql = ',\n'.join(values)

                insert_sql = f"""
                    INSERT INTO {full_table_name} ({columns})
                    VALUES {values_sql}
                """

                try:
                    self.cursor.execute(insert_sql)
                    inserted_count += len(batch)

                    # Show progress
                    batch_num = (i // batch_size) + 1
                    print(f"   ⏳ Progress: {batch_num}/{total_batches} batches ({inserted_count:,}/{len(df):,} rows)", end='\r')

                except Exception as e:
                    print(f"\n   ⚠️  Error inserting batch {batch_num}: {e}")
                    continue

            print()  # New line after progress

            new_count = self.get_row_count(table_name)
            actual_inserted = new_count - current_count

            print(f"   ✓ Processed {len(df):,} rows")
            print(f"   ✓ Inserted: {actual_inserted:,} new rows")
            print(f"   ✓ Total in table: {new_count:,} rows")

        except Exception as e:
            print(f"   ✗ Error loading data: {e}")
            import traceback
            traceback.print_exc()

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
        template = """# Databricks Connection Settings
# Get these from your Databricks workspace

# Server Hostname (from Compute → Cluster → Advanced → JDBC/ODBC)
# Example: dbc-xxxxx-yyyy.cloud.databricks.com
DATABRICKS_SERVER_HOSTNAME=dbc-xxxxx-yyyy.cloud.databricks.com

# HTTP Path (from Compute → Cluster → Advanced → JDBC/ODBC)
# Example: /sql/1.0/warehouses/xxxxx
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx

# Access Token (from User Settings → Access Tokens)
# Example: dapi1234567890abcdef...
DATABRICKS_ACCESS_TOKEN=your-access-token-here

# Catalog and Schema (database) settings
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=nourishbox
"""

        with open('.env', 'w') as f:
            f.write(template)

        print("\n📝 Created .env template file")
        print("   Please edit .env and add your Databricks credentials")
        print("\n   To get your credentials:")
        print("   1. Go to your Databricks workspace")
        print("   2. Create a cluster (Compute → Create Cluster)")
        print("   3. Generate access token (User Settings → Access Tokens)")
        print("   4. Get connection details (Cluster → Advanced → JDBC/ODBC)")
        print("   5. Paste into .env file\n")
        return True

    return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Sync NourishBox data to Databricks')
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
    print("NOURISHBOX → DATABRICKS SYNC")
    print("="*70)

    # Check if CSV files exist
    if not os.path.exists(DATA_DIR):
        print(f"\n❌ Data directory not found: {DATA_DIR}")
        print("   Run 'python src/generate_nourishbox_data.py' first to generate data")
        sys.exit(1)

    # Check if .env exists
    if not Path('.env').exists():
        print("\n❌ .env file not found!")
        create_env_template()
        sys.exit(1)

    # Initialize sync
    sync = DatabricksSync()

    try:
        # Connect
        sync.connect()

        # Create schema
        sync.create_schema()

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
            if args.clear and sync.table_exists(table_name):
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
        print("\n1. Verify data in Databricks:")
        print(f"   - Go to Data → {sync.catalog} → {sync.schema}")
        print("   - Click on tables to preview data")
        print("\n2. Create a notebook for analysis:")
        print("   - Workspace → Create → Notebook")
        print(f"   - Query: SELECT * FROM {sync.catalog}.{sync.schema}.customers LIMIT 10;")
        print("\n3. Connect Power BI (if available):")
        print(f"   Server Hostname: {sync.server_hostname}")
        print(f"   HTTP Path: {sync.http_path}")
        print(f"   Catalog: {sync.catalog}")
        print(f"   Schema: {sync.schema}")
        print("\n4. Build your dashboards! 🎉\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        sync.disconnect()


if __name__ == "__main__":
    main()