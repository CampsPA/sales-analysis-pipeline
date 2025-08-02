# Sales Analytics ETL Pipeline

This project demonstrates an end-to-end workflow that starts with messy sales data from Kaggle, cleans and analyzes it in Excel, then uses Python scripts to import the cleaned data into PostgreSQL for further analysis. Finally, it exports the database tables as CSV files for visualization and reporting in Power BI.

---

## Project Overview

- Clean and analyze raw sales data from Kaggle using Excel  
- Use Python to import cleaned Excel files into PostgreSQL  
- Perform further analysis and normalization within PostgreSQL  
- Export PostgreSQL tables as timestamped CSV files  
- Use CSV files as data sources for Power BI reports and dashboards (in progress...)

---

## Technologies Used

- Excel (data cleaning and preliminary analysis)  
- Python (Pandas, SQLAlchemy)  
- PostgreSQL  
- Power BI

---

## Repository Structure
/data/ # Raw and cleaned Excel files
/sql/ # SQL query images or scripts
/scripts/
import_excel_to_sql.py # Script to import cleaned Excel data into PostgreSQL
export_sql_to_csv.py # Script to export PostgreSQL tables to CSV for Power BI
/outputs/ # Exported CSV files for Power BI
README.md # Project documentation


---

## How to Use

1. Ensure PostgreSQL is installed and running locally.  
2. Create a database named `sales_analysis`.  
3. Update database credentials in the Python scripts if needed.  
4. Clean and prepare the data in Excel as needed (already done here).  
5. Run `import_excel_to_sql.py` to import cleaned Excel data into PostgreSQL.  
6. Run `export_sql_to_csv.py` to export database tables as CSV files for Power BI.  
7. Load the CSV files into Power BI to build reports and dashboards.

---

## Contact

Feel free to reach out for questions or feedback!

---

*This project showcases a practical ETL pipeline integrating Excel, Python, PostgreSQL, and Power BI for data analytics.*


