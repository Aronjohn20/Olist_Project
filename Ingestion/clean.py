import os
import numpy as np
import pandas as pd

print("Data cleaning started.")

os.makedirs("Dataset/cleaned", exist_ok=True)

customers = pd.read_csv("Dataset/olist_customers_dataset.csv")
orders = pd.read_csv("Dataset/olist_orders_dataset.csv")
order_payments = pd.read_csv("Dataset/olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("Dataset/olist_order_reviews_dataset.csv")
sellers = pd.read_csv("Dataset/olist_sellers_dataset.csv")
products = pd.read_csv("Dataset/olist_products_dataset.csv")
categories = pd.read_csv("Dataset/product_category_name_translation.csv")

# Customers
customers["customer_zip_code_prefix"] = customers["customer_zip_code_prefix"].astype(str).str.strip().str.zfill(5)
customers["customer_city"] = customers["customer_city"].str.strip().str.lower()
customers["customer_state"] = customers["customer_state"].str.strip().str.upper()

# Orders
for col in [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")
orders["order_status"] = orders["order_status"].str.strip().str.lower()

# Order Payments
order_payments["payment_type"] = order_payments["payment_type"].str.strip().str.lower()
order_payments = order_payments[~((order_payments["payment_type"] == "not_defined") & (order_payments["payment_value"] == 0))].copy()
order_payments["payment_installments"] = order_payments["payment_installments"].clip(lower=1).astype(int)

# Order Reviews
order_reviews["review_creation_date"] = pd.to_datetime(order_reviews["review_creation_date"], errors="coerce")
order_reviews["review_answer_timestamp"] = pd.to_datetime(order_reviews["review_answer_timestamp"], errors="coerce")
order_reviews = order_reviews.drop(columns=["review_comment_title", "review_comment_message"])

# Sellers
sellers["seller_zip_code_prefix"] = sellers["seller_zip_code_prefix"].astype(str).str.strip().str.zfill(5)
sellers["seller_city"] = sellers["seller_city"].str.strip().str.lower()
sellers["seller_state"] = sellers["seller_state"].str.strip().str.upper()

# Products
products = products.rename(columns={
    "product_name_lenght": "product_name_length",
    "product_description_lenght": "product_description_length",
})
products["product_category_name"] = products["product_category_name"].fillna("unknown").str.strip().str.lower()
for col in ["product_name_length", "product_description_length", "product_photos_qty"]:
    products[col] = products[col].fillna(0).astype(int)
for col in ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]:
    products[col] = products[col].replace(0, np.nan)
    products[col] = products[col].fillna(products[col].median())

# Categories
categories["product_category_name"] = categories["product_category_name"].str.strip().str.lower()
categories["product_category_name_english"] = categories["product_category_name_english"].str.strip().str.lower()
extra_categories = pd.DataFrame([
    {"product_category_name": "unknown", "product_category_name_english": "unknown"},
    {"product_category_name": "pc_gamer", "product_category_name_english": "pc_gamer"},
    {"product_category_name": "portateis_cozinha_e_preparadores_de_alimentos", "product_category_name_english": "small_appliances_kitchen_food_preparers"},
])
categories = pd.concat([categories, extra_categories], ignore_index=True).drop_duplicates(subset=["product_category_name"])

# Save to CSV
customers.to_csv("Dataset/cleaned/olist_customers_clean.csv", index=False)
orders.to_csv("Dataset/cleaned/olist_orders_clean.csv", index=False)
order_payments.to_csv("Dataset/cleaned/olist_order_payments_clean.csv", index=False)
order_reviews.to_csv("Dataset/cleaned/olist_order_reviews_clean.csv", index=False)
sellers.to_csv("Dataset/cleaned/olist_sellers_clean.csv", index=False)
products.to_csv("Dataset/cleaned/olist_products_clean.csv", index=False)
categories.to_csv("Dataset/cleaned/product_category_name_translation_clean.csv", index=False)

print("Data cleaning completed.")