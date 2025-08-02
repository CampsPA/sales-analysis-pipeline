# This script imports data from a database and converts to CSV so later it can be exported into Power BI
# Need to import psycopg2-binary to run properly
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os

# Create a main function.
def main():
    # Connect to a database.
    username='postgres'
    password = 'Campospa'
    host = 'localhost'
    port = '5433'
    database = 'sales_analysis'

    # Create the SQLAlchemy engine
    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")


    # Create a list to store the database tables.
    tables =  ['customers', 'order_details', 'orders', 'products']

    # Export to the directory.
    export_dir = r'C:\Users\campo\OneDrive\Desktop\Excel Data Analysis\Projects\Sales_Analytics_Portfolio_Project\Database_csv_files'
    os.makedirs(export_dir, exist_ok=True)

    # Create a timestamp for versioned exports.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Export each table to CSV.
    try:
        for table in tables:
            df = pd.read_sql_table(table, con=engine)
            output_path = os.path.join(export_dir, f"{table}_{timestamp}.csv")
            df.to_csv(output_path, index=False)
            print(f"✅ Exported {table} to {output_path}")


        # Print a success message.
        print('Data export complete.')

    except Exception as e:
        print("Error during export:", e)


 # Call the main function.
if __name__ == '__main__':
    main()