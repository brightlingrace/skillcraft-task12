import pandas as pd

# Run this script in the folder containing raw_orders_messy.csv
INPUT_FILE = "raw_orders_messy.csv"
OUTPUT_FILE = "cleaned_orders.csv"
df = pd.read_csv(INPUT_FILE)
print("Initial shape:", df.shape)
for col in ["Customer_ID", "City", "Category", "Payment_Status"]:
    df[col] = df[col].astype("string").str.strip()
df["City"] = df["City"].str.title()
df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True, errors="coerce")
df["Order_Value"] = pd.to_numeric(df["Order_Value"], errors="coerce")
df = df.drop_duplicates(subset=["Customer_ID", "Order_ID", "Order_Date"], keep="first")
df["Customer_ID"] = df["Customer_ID"].fillna("UNKNOWN")
for col in ["City", "Category", "Payment_Status"]:
    df[col] = df[col].fillna("Unknown")
df["Order_Value"] = df["Order_Value"].fillna(df["Order_Value"].median())
df = df.dropna(subset=["Order_Date"])
df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
df.to_csv(OUTPUT_FILE, index=False)
print("Cleaned shape:", df.shape, "| missing cells:", int(df.isna().sum().sum()))
