"""
### Project: Sales Analytics System
### Name: Siddharth Godbole
### Roll / Enrollment ID: BITSom_ba_25071865
"""

### Sales Analytics System
### Module 3 – Python Programming Assignment

### 1. Project Overview
This project is created as part of the Module 3 Python assignment.
The aim of this project is to build a small sales analytics system that can handle messy real-world sales data, clean it, analyze it, connect it with an external API, and finally generate a professional business report.

### Instead of directly using the raw file, the project follows a proper data processing pipeline similar to what is used in companies:

Reading raw data
Cleaning and validating it
Performing sales analysis
Enriching data using an API
Generating reports for decision making
### 2. Dataset Used
The input file used in this project is:

data/sales_data.txt

Each line in this file represents one sales transaction and contains the following fields:

TransactionID | Date | ProductID | ProductName | Quantity | UnitPrice | CustomerID | Region

Example: T018|2024-12-29|P107|USB Cable|8|173|C009|South

The dataset intentionally contains issues like:

Commas inside product names
Commas inside numeric values
Missing fields
Zero or negative values
Invalid transaction IDs
These issues are handled by the cleaning logic in the project.

### 3. Project Folder Structure
sales-analytics-system │ ├── main.py ├── README.md ├── requirements.txt │ ├── utils │ ├── file_handler.py │ ├── data_processor.py │ └── api_handler.py │ ├── data │ ├── sales_data.txt │ └── enriched_sales_data.txt │ └── output └── sales_report.txt

Each file has a clear purpose:

file_handler.py → Reads the sales file and handles encoding issues
data_processor.py → Cleans data, validates it, performs analysis and enrichment
api_handler.py → Fetches product data from the external API
main.py → Runs the full application flow
### 4. How the System Works
When main.py is executed, the following steps are performed:

The sales data file is read while handling different file encodings.
The raw data is cleaned and invalid records are removed.
The user is shown available regions and can optionally filter the data.
Sales analytics such as revenue, top products, customers and daily trends are calculated.
Product information is fetched from the DummyJSON API.
Sales data is enriched using the API product details.
Enriched data is saved to data/enriched_sales_data.txt.
A professional sales report is generated in output/sales_report.txt.
This flow ensures that raw data is converted into meaningful business insights.

### 5. API Used
This project uses the DummyJSON Products API:

### https://dummyjson.com/products

It provides product information such as:

Title
Category
Brand
Rating
These fields are added to the sales data during the enrichment process.

### 6. How to Run the Project
Open a terminal inside the project folder
Make sure Python is installed
Install required libraries:
pip install requests 4. Run the program:

After execution, the enriched data file and the sales report will be generated automatically.

### 7. Output Files
After running the program, two important files are created:

data/enriched_sales_data.txt
Contains the original sales data along with API fields like category, brand, rating and match status.

output/sales_report.txt
Contains a detailed formatted sales report including:

### Overall summary
Region-wise performance
Top products and customers
Daily sales trend
API enrichment summary
### 8. Conclusion
This project demonstrates how Python can be used to build a complete data processing and analytics pipeline.
It combines file handling, data cleaning, business analytics, API integration and reporting into a single working system, similar to how real-world sales analytics applications are built.