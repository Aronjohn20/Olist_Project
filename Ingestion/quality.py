import pandas as pd

print("Data validation started.\n")

# Load the cleaned files you saved in the previous step
customers = pd.read_csv("Dataset/cleaned/olist_customers_clean.csv", dtype={"customer_zip_code_prefix": str})
orders = pd.read_csv("Dataset/cleaned/olist_orders_clean.csv")
order_payments = pd.read_csv("Dataset/cleaned/olist_order_payments_clean.csv")
order_reviews = pd.read_csv("Dataset/cleaned/olist_order_reviews_clean.csv")
sellers = pd.read_csv("Dataset/cleaned/olist_sellers_clean.csv", dtype={"seller_zip_code_prefix": str})
products = pd.read_csv("Dataset/cleaned/olist_products_clean.csv")
categories = pd.read_csv("Dataset/cleaned/product_category_name_translation_clean.csv")

# Convert date columns back to datetime (CSV files store dates as plain text)
for col in [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

order_reviews["review_creation_date"] = pd.to_datetime(order_reviews["review_creation_date"], errors="coerce")
order_reviews["review_answer_timestamp"] = pd.to_datetime(order_reviews["review_answer_timestamp"], errors="coerce")


# ==============================================================================
# CHECK 1: Duplicate Reviews per Order (Prevents Double-Counting Revenue)
# ==============================================================================
before_reviews = len(order_reviews)
order_reviews = (
    order_reviews.sort_values("review_answer_timestamp")
    .drop_duplicates(subset=["order_id"], keep="last")
    .reset_index(drop=True)
)
print(f"[Check 1 - Reviews] Removed {before_reviews - len(order_reviews)} duplicate order reviews.")


# ==============================================================================
# CHECK 2: Impossible Order Timelines (Prevents Negative Delivery Times)
# ==============================================================================
orders["is_valid_delivery_timeline"] = (
    (orders["order_status"] == "delivered")
    & orders["order_delivered_customer_date"].notna()
    & (orders["order_delivered_customer_date"] >= orders["order_purchase_timestamp"])
)
bad_timelines = ((orders["order_status"] == "delivered") & (~orders["is_valid_delivery_timeline"])).sum()
print(f"[Check 2 - Orders] Flagged {bad_timelines} 'delivered' orders with missing or impossible delivery dates.")


# ==============================================================================
# CHECK 3: Orphan Foreign Keys (Checks if Any Links Between Tables Are Broken)
# ==============================================================================
missing_customers = (~orders["customer_id"].isin(customers["customer_id"])).sum()
missing_payment_orders = (~order_payments["order_id"].isin(orders["order_id"])).sum()
missing_review_orders = (~order_reviews["order_id"].isin(orders["order_id"])).sum()
missing_categories = (~products["product_category_name"].isin(categories["product_category_name"])).sum()

print(f"[Check 3 - Links] Orphan customer_ids in orders: {missing_customers}")
print(f"[Check 3 - Links] Orphan order_ids in payments:   {missing_payment_orders}")
print(f"[Check 3 - Links] Orphan order_ids in reviews:    {missing_review_orders}")
print(f"[Check 3 - Links] Unmapped categories in products: {missing_categories}")


# ==============================================================================
# CHECK 4: Zero or Negative Payment Values
# ==============================================================================
zero_payments = (order_payments["payment_value"] <= 0).sum()
print(f"[Check 4 - Payments] Found {zero_payments} payment rows with value <= 0 (100% voucher discounts).")


# ==============================================================================
# Save updated reviews and orders back to Dataset/cleaned/
# ==============================================================================
orders.to_csv("Dataset/cleaned/olist_orders_clean.csv", index=False)
order_reviews.to_csv("Dataset/cleaned/olist_order_reviews_clean.csv", index=False)
order_payments.to_csv("Dataset/cleaned/olist_order_payments_clean.csv", index=False)
products.to_csv("Dataset/cleaned/olist_products_clean.csv", index=False)
print("\nValidation complete and updated files saved.")