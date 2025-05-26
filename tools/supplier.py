# tools/supplier.py

import pandas as pd
from data.db import fetch_table


def analyze_supplier_performance():
    df = fetch_table("supplier_orders")
    summary = df.groupby("supplier_name").agg({
        "delayed": lambda x: round((x.sum() / len(x)) * 100, 2),
        "cost_per_unit": ["mean", "std"]
    }).reset_index()

    summary.columns = ["supplier_name", "delay_rate_%", "avg_price", "price_volatility"]
    summary["avg_price"] = summary["avg_price"].round(2)
    summary["price_volatility"] = summary["price_volatility"].round(2)

    return summary.sort_values("delay_rate_%", ascending=True)


# def supplier_performance_summary():
def supplier_performance_summary(_=None):

    summary_df = analyze_supplier_performance()
    if summary_df.empty:
        return "No supplier order data available."

    text = "\U0001f69a Supplier Performance:\n"
    for _, row in summary_df.iterrows():
        text += (
            f"- {row['supplier_name']}: "
            f"{row['delay_rate_%']}% late deliveries, "
            f"Avg Price = ${row['avg_price']}, "
            f"Volatility = ±${row['price_volatility']}\n"
        )
    return text
