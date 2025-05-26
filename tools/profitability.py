# tools/profitability.py

import pandas as pd
from data.db import fetch_table


def compute_dish_profitability(_=None):
    recipe_df = fetch_table("recipe_data")
    ingredient_cost_df = fetch_table("ingredient_prices")
    menu_df = fetch_table("menu_prices")

    merged = pd.merge(recipe_df, ingredient_cost_df, on="ingredient", how="left")
    merged["ingredient_cost"] = merged["qty_per_unit"] * merged["cost_per_unit"]

    dish_cost = merged.groupby("item_name")["ingredient_cost"].sum().reset_index()
    dish_cost.rename(columns={"ingredient_cost": "total_cost"}, inplace=True)

    final_df = pd.merge(dish_cost, menu_df, on="item_name")
    final_df["profit"] = final_df["selling_price"] - final_df["total_cost"]
    final_df["margin_%"] = (final_df["profit"] / final_df["selling_price"] * 100).round(2)

    return final_df.sort_values(by="margin_%")


def low_margin_dishes(_=None):  # ✅ LangChain-compatible
    threshold = 30  # default cutoff
    df = compute_dish_profitability()

    # ✅ Ensure numeric types
    df["margin_%"] = pd.to_numeric(df["margin_%"], errors="coerce")
    low_margin = df[df["margin_%"] < float(threshold)]

    if low_margin.empty:
        return "All dishes are within acceptable profit margins."

    text = "\u26a0\ufe0f Dishes with Low Profit Margin:\n"
    for _, row in low_margin.iterrows():
        text += (
            f"- {row['item_name']}: {row['margin_%']}% margin "
            f"(Cost: ${row['total_cost']:.2f}, Price: ${row['selling_price']})\n"
        )
    return text
