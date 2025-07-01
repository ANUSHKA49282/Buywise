# backend/forecast.py
import pandas as pd

def get_forecast():
    try:
        df = pd.read_csv("data/inventory.csv")

        # Make sure required columns exist
        required_cols = {"StoreID", "SKU", "ProductName", "CurrentStock", "WeeklySales"}
        if not required_cols.issubset(df.columns):
            return {"error": "Missing one or more required columns in inventory.csv"}

        transfers = []

        for sku in df["SKU"].unique():
            sku_df = df[df["SKU"] == sku].copy()

            # Safely parse WeeklySales column
            sku_df["WeeklySales"] = sku_df["WeeklySales"].apply(lambda x: eval(x) if isinstance(x, str) else x)
            sku_df["AvgSales"] = sku_df["WeeklySales"].apply(lambda x: sum(x) / len(x))

            surplus = sku_df[sku_df["CurrentStock"] > sku_df["AvgSales"] * 2]
            shortage = sku_df[sku_df["CurrentStock"] < sku_df["AvgSales"] * 0.75]

            for _, short_row in shortage.iterrows():
                for _, surplus_row in surplus.iterrows():
                    qty = int(min(
                        surplus_row["CurrentStock"] - surplus_row["AvgSales"],
                        short_row["AvgSales"] - short_row["CurrentStock"]
                    ))

                    if qty > 0:
                        transfers.append({
                            "SKU": sku,
                            "Product": short_row["ProductName"],
                            "FromStore": surplus_row["StoreID"],
                            "ToStore": short_row["StoreID"],
                            "SuggestedTransferQty": qty
                        })

        return {"transfers": transfers}

    except Exception as e:
        return {"error": str(e)}
