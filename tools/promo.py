# tools/promo.py

import pandas as pd
from data.db import fetch_table


def analyze_promo_effectiveness():
    sales_df = fetch_table("sales_data")
    promo_df = fetch_table("promo_data")
    results = []

    for _, promo in promo_df.iterrows():
        item = promo["item_name"]
        name = promo["promo_name"]
        start = pd.to_datetime(promo["start_date"]).date()
        end = pd.to_datetime(promo["end_date"]).date()
        channel = promo["channel"]

        before = sales_df[
            (sales_df["item_name"] == item) &
            (sales_df["sale_date"] < start)
        ]["quantity"].sum()

        during = sales_df[
            (sales_df["item_name"] == item) &
            (sales_df["sale_date"] >= start) &
            (sales_df["sale_date"] <= end)
        ]["quantity"].sum()

        uplift = during - before
        uplift_pct = (uplift / before * 100) if before > 0 else 0

        results.append({
            "promo_name": name,
            "item": item,
            "channel": channel,
            "before_sales": before,
            "during_sales": during,
            "uplift": uplift,
            "uplift_%": round(uplift_pct, 2)
        })

    return pd.DataFrame(results).sort_values(by="uplift_%", ascending=False)


# def promo_summary_text():
def promo_summary_text(_=None):

    df = analyze_promo_effectiveness()
    if df.empty:
        return "No promotion data available."

    text = "\U0001f4e3 Promo Effectiveness:\n"
    for _, row in df.iterrows():
        text += (
            f"- {row['promo_name']} ({row['item']} via {row['channel']}): "
            f"{row['uplift_%']}% uplift in sales "
            f"(Before: {row['before_sales']}, During: {row['during_sales']})\n"
        )
    return text