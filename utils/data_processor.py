# =====================================
# PART 1: PARSING AND CLEANING
# Task 1.2
# =====================================
# Parse raw sales data and clean invalid or corrupted records

def parse_and_clean_data(raw_lines):
    """
    This function takes raw data lines
    and converts them into clean records.
    Invalid records are skipped.
    """

    cleaned_data = []    
    invalid_count = 0    

    for line in raw_lines:
        # split each line using pipe symbol
        parts = line.split("|")

        # if number of columns is not correct, skip
        if len(parts) != 8:
            invalid_count += 1
            continue

        # unpack all columns
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Apply validation rules for transaction ID, product ID and numeric fields

        # Product ID must start with 'P'
        if not product_id.startswith("P"):
            invalid_count += 1
            continue


        # transaction id must start with 'T'
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        # customer id and region should not be empty
        if customer_id.strip() == "" or region.strip() == "":
            invalid_count += 1
            continue

        # remove comma from product name
        product_name = product_name.replace(",", " ")

        # remove commas from numeric values
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            # convert quantity and price to numbers
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            invalid_count += 1
            continue

        # quantity and price must be greater than zero
        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        # create cleaned record as dictionary
        record = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        # add valid record to list
        cleaned_data.append(record)

    # return cleaned data and invalid count
    return cleaned_data, invalid_count


# =====================================
# PART 1: VALIDATION AND FILTERING
# Task 1.3
# =====================================
# Allow optional filtering of sales data based on region

def validate_and_filter_sales(cleaned_data):
    """
    This function allows user to filter
    already cleaned data based on region.
    """

    # collect unique regions from data
    regions = set()
    for record in cleaned_data:
        regions.add(record["Region"])

    # show available regions to user
    print("\nAvailable Regions:")
    for region in regions:
        print("-", region)

    # ask user if filtering is required
    choice = input("\nDo you want to filter data by region? (yes/no): ").strip().lower()

    # if user does not want filter
    if choice != "yes":
        summary = {
            "filter_applied": False,
            "total_records": len(cleaned_data)
        }
        return cleaned_data, summary

    # take region input from user
    selected_region = input("Enter region name: ").strip()

    filtered_data = []

    # filter records based on selected region
    for record in cleaned_data:
        if record["Region"].lower() == selected_region.lower():
            filtered_data.append(record)

    # prepare filter summary
    summary = {
        "filter_applied": True,
        "region": selected_region,
        "records_before_filter": len(cleaned_data),
        "records_after_filter": len(filtered_data)
    }

    return filtered_data, summary

# =====================================
# PART 2: DATA PROCESSING
# This section contains all business level analytics
# like revenue, region performance, product sales etc.
# =====================================
# Sales analytics functions for revenue, trends and performance analysis

def calculate_total_revenue(transactions):
    """
    This function calculates the overall revenue
    of the company from all valid transactions.
    Formula used:
    Revenue = Quantity * UnitPrice
    """

    total = 0

    # Loop through each transaction
    for t in transactions:
        # For every transaction multiply quantity and price
        total += t["Quantity"] * t["UnitPrice"]

    return total


def region_wise_sales(transactions):
    """
    This function calculates sales performance
    for each region (North, South, East, West).

    It returns total sales, transaction count
    and percentage contribution of each region.
    """

    region_data = {}

    # First calculate overall revenue
    total_revenue = calculate_total_revenue(transactions)

    # Loop through each transaction
    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        # If region not yet added, initialize it
        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        # Add revenue and increase transaction count
        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Calculate percentage contribution of each region
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort regions by total sales (highest first)
    return dict(sorted(region_data.items(),
                       key=lambda x: x[1]["total_sales"],
                       reverse=True))


def top_selling_products(transactions, n=5):
    """
    This function finds top N products
    based on total quantity sold.

    It also calculates total revenue for each product.
    """

    product_map = {}

    # Aggregate quantity and revenue for each product
    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_map:
            product_map[name] = {"qty": 0, "rev": 0}

        product_map[name]["qty"] += qty
        product_map[name]["rev"] += revenue

    # Convert dictionary into list of tuples
    result = []
    for name, data in product_map.items():
        result.append((name, data["qty"], data["rev"]))

    # Sort by quantity sold (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    """
    This function analyzes customer behavior.

    For each customer it calculates:
    - total amount spent
    - number of purchases
    - average order value
    - unique products bought
    """

    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        # If customer not yet added, initialize
        if cid not in customers:
            customers[cid] = {
                "total_spent": 0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(t["ProductName"])

    # Convert into final output format
    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(data["total_spent"] / data["purchase_count"], 2),
            "products_bought": list(data["products_bought"])
        }

    # Sort customers by total spent (highest first)
    return dict(sorted(result.items(),
                       key=lambda x: x[1]["total_spent"],
                       reverse=True))


def daily_sales_trend(transactions):
    """
    This function groups all transactions
    by date and calculates daily performance:
    - total revenue
    - number of transactions
    - number of unique customers
    """

    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(t["CustomerID"])

    # Convert into final readable format
    final = {}
    for date, data in daily.items():
        final[date] = {
            "revenue": round(data["revenue"], 2),
            "transaction_count": data["transaction_count"],
            "unique_customers": len(data["customers"])
        }

    return dict(sorted(final.items()))


def find_peak_sales_day(transactions):
    """
    This function finds the date
    on which the company earned maximum revenue.
    """

    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0
    peak_count = 0

    for date, data in daily.items():
        if data["revenue"] > peak_revenue:
            peak_revenue = data["revenue"]
            peak_date = date
            peak_count = data["transaction_count"]

    return (peak_date, peak_revenue, peak_count)


def low_performing_products(transactions, threshold=10):
    """
    This function identifies products
    whose total quantity sold is below the threshold.
    """

    product_map = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_map:
            product_map[name] = {"qty": 0, "rev": 0}

        product_map[name]["qty"] += qty
        product_map[name]["rev"] += revenue

    low = []
    for name, data in product_map.items():
        if data["qty"] < threshold:
            low.append((name, data["qty"], data["rev"]))

    # Sort by quantity (lowest first)
    low.sort(key=lambda x: x[1])

    return low


# =====================================
# PART 3: API DATA ENRICHMENT
# =====================================
# Enrich cleaned sales data using external API product information

def enrich_sales_data(transactions, product_mapping):
    """
    This function enriches internal sales data
    using product information fetched from API.

    It adds:
    - API_Category
    - API_Brand
    - API_Rating
    - API_Match (True / False)
    """

    enriched = []

    for t in transactions:

        # Example: P101 → 101
        product_id_raw = t["ProductID"]
        numeric_id = int(product_id_raw.replace("P", "")) - 100


        # Check if this product exists in API data
        api_product = product_mapping.get(numeric_id)

        enriched_record = t.copy()

        # If product is found in API
        if api_product:
            enriched_record["API_Category"] = api_product["category"]
            enriched_record["API_Brand"] = api_product["brand"]
            enriched_record["API_Rating"] = api_product["rating"]
            enriched_record["API_Match"] = True
        else:
            # If no matching product found in API
            enriched_record["API_Category"] = None
            enriched_record["API_Brand"] = None
            enriched_record["API_Rating"] = None
            enriched_record["API_Match"] = False

        enriched.append(enriched_record)

    return enriched

import datetime
# Generate formatted sales analytics report for business users
def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    This function generates a complete
    sales analytics report in text format.

    The report is written in a professional,
    management style as required in the assignment.
    """

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ----------------------------------
    # Calculate all required analytics
    # ----------------------------------

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)

    # Date range
    dates = [t["Date"] for t in transactions]
    start_date = min(dates)
    end_date = max(dates)

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily = daily_sales_trend(transactions)
    peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API enrichment summary
    total_enriched = sum(1 for t in enriched_transactions if t["API_Match"])
    success_rate = round((total_enriched / len(enriched_transactions)) * 100, 2)

    not_enriched = [t["ProductName"] for t in enriched_transactions if not t["API_Match"]]

    # ----------------------------------
    # Start writing report
    # ----------------------------------

    with open(output_file, "w", encoding="utf-8") as file:

        file.write("============================================\n")
        file.write("SALES ANALYTICS REPORT\n")
        file.write(f"Generated: {now}\n")
        file.write(f"Records Processed: {total_transactions}\n")
        file.write("============================================\n\n")

        # OVERALL SUMMARY
        file.write("OVERALL SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions: {total_transactions}\n")
        file.write(f"Average Order Value: ₹{(total_revenue/total_transactions):,.2f}\n")
        file.write(f"Date Range: {start_date} to {end_date}\n\n")

        # REGION WISE PERFORMANCE
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("--------------------------------------------\n")
        file.write("Region | Total Sales | % of Total | Transactions\n")

        for region, data in region_data.items():
            file.write(f"{region} | ₹{data['total_sales']:,.2f} | {data['percentage']}% | {data['transaction_count']}\n")

        file.write("\n")

        # TOP PRODUCTS
        file.write("TOP 5 PRODUCTS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | Product | Quantity | Revenue\n")

        rank = 1
        for name, qty, rev in top_products:
            file.write(f"{rank} | {name} | {qty} | ₹{rev:,.2f}\n")
            rank += 1

        file.write("\n")

        # TOP CUSTOMERS
        file.write("TOP 5 CUSTOMERS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | CustomerID | Total Spent | Orders\n")

        rank = 1
        for cid, data in list(customers.items())[:5]:
            file.write(f"{rank} | {cid} | ₹{data['total_spent']:,.2f} | {data['purchase_count']}\n")
            rank += 1

        file.write("\n")

        # DAILY SALES TREND
        file.write("DAILY SALES TREND\n")
        file.write("--------------------------------------------\n")
        file.write("Date | Revenue | Transactions | Customers\n")

        for date, data in daily.items():
            file.write(f"{date} | ₹{data['revenue']:,.2f} | {data['transaction_count']} | {data['unique_customers']}\n")

        file.write("\n")

        # PRODUCT PERFORMANCE
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("--------------------------------------------\n")
        file.write(f"Best Selling Day: {peak_date} (₹{peak_revenue:,.2f} in {peak_count} transactions)\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"{name} - Qty: {qty}, Revenue: ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")

        file.write("\n")

        # API ENRICHMENT SUMMARY
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Products Enriched: {total_enriched}/{len(enriched_transactions)}\n")
        file.write(f"Success Rate: {success_rate}%\n")

        if not_enriched:
            file.write("Products not enriched:\n")
            for p in set(not_enriched):
                file.write(f"- {p}\n")
        else:
            file.write("All products were enriched successfully.\n")

    print("Sales report generated at:", output_file)
