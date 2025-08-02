# Create a script to import excel files into postgreSQL

import pandas as pd
from sqlalchemy import create_engine, text


def main():
    # Create connection to PostgreSQL
    username = 'postgres'
    password = 'Campospa'
    host = 'localhost'
    port = '5433'
    database = 'sales_analysis'  # Create database manually in postgres

    # Create database engine.
    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

    try:
        # Load Excel file
        df = pd.read_excel(r"C:\Users\campo\OneDrive\Desktop\Excel Data Analysis\Projects\Sales_Analytics_Portfolio_Plan\Clean_sales_data.xlsx")
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

        # Convert date columns
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', dayfirst=True)
        df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce', dayfirst=True)

        # Round numeric values to 2 decimals.
        df['sales'] = df['sales'].round(2)
        df['profit'] = df['profit'].round(2)
        df['discount'] = df['discount'].round(2)
        df['shipping_cost'] = df['shipping_cost'].round(2)

        print("Excel file loaded successfully.")

    except Exception as e:
        print("Failed to load Excel file:", e)
        exit()

    try:
        # Create a staging table and normalize Tables automatically
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS sales_data (
            row_id SERIAL PRIMARY KEY,
            order_id VARCHAR,
            order_date DATE,
            ship_date DATE,
            ship_mode VARCHAR,
            customer_id VARCHAR,
            customer_name VARCHAR,
            segment VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR,
            postal_code VARCHAR,
            market VARCHAR,
            region VARCHAR,
            product_id VARCHAR,
            category VARCHAR,
            sub_category VARCHAR,
            product_name TEXT,
            sales NUMERIC(12, 2),
            quantity INTEGER,
            discount NUMERIC(12, 2),
            profit NUMERIC(12, 2),
            shipping_cost NUMERIC(12, 2),
            order_priority VARCHAR
        );

        CREATE TABLE IF NOT EXISTS customers (  
            customer_id VARCHAR PRIMARY KEY,
            customer_name VARCHAR,
            segment VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR,
            postal_code VARCHAR,
            region VARCHAR
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR PRIMARY KEY,
            product_name TEXT,
            category VARCHAR,
            sub_category VARCHAR
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR PRIMARY KEY,
            order_date DATE,
            ship_date DATE,
            ship_mode VARCHAR,
            customer_id VARCHAR REFERENCES customers(customer_id),
            market VARCHAR,
            order_priority VARCHAR
        );


        CREATE TABLE IF NOT EXISTS order_details (
            row_id SERIAL PRIMARY KEY,
            order_id VARCHAR REFERENCES orders(order_id),
            product_id VARCHAR REFERENCES products(product_id),
            sales NUMERIC,
            quantity INTEGER,
            discount NUMERIC,
            profit NUMERIC,
            shipping_cost NUMERIC
        );
        """

        with engine.begin() as conn:
            conn.execute(text(create_tables_sql))
            print("All tables created successfully.")
    except Exception as e:
        print("Failed to create tables:", e)
        exit()

    try:
        # Load data into the staging table.
        df.to_sql("sales_data", engine, index=False, if_exists="replace")
        print("Data loaded into staging table: sales_data")
    except Exception as e:
        print("Failed to load data into staging table:", e)
        exit()

    try:
        # Populate Normalized Tables.
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO customers (customer_id, customer_name, segment, city, state, country, postal_code, region)
                SELECT DISTINCT customer_id, customer_name, segment, city, state, country, postal_code, region
                FROM sales_data
                ON CONFLICT (customer_id) DO NOTHING;

            """))

            conn.execute(text("""
                INSERT INTO products (product_id, product_name, category, sub_category)
                SELECT DISTINCT product_id, product_name, category, sub_category
                FROM sales_data
                ON CONFLICT (product_id) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO orders (order_id, order_date, ship_date, ship_mode, customer_id, market, order_priority)
                SELECT DISTINCT order_id, order_date, ship_date, ship_mode, customer_id, market, order_priority
                FROM sales_data
                ON CONFLICT (order_id) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO order_details (order_id, product_id, sales, quantity, discount, profit, shipping_cost)
                SELECT order_id, product_id, sales, quantity, discount, profit, shipping_cost
                FROM sales_data;
            """))
            print("Data inserted into normalized tables.")

    except Exception as e:
        print("Failed to insert data into normalized tables:", e)
        exit()

    # Drop staging table.
    try:
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS sales_data;"))
            print("Staging table dropped.")
    except Exception as e:
        print("Failed to drop staging table:", e)
        print(" ETL process completed successfully.")


# Run the main function.
if __name__ == '__main__':
    main()

