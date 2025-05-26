# tools/pricing.py

import pandas as pd
from data.db import fetch_table


#def dynamic_price_recommendation():
def dynamic_price_recommendation(_=None):

    recipe_df = fetch_table("recipe_data")
    ingredient_price_df = fetch_table("ingredient_prices")
    menu_df = fetch_table("menu_prices")
    trend_df = fetch_table("ingredient_trends")
    sales_df = fetch_table("sales_summary")

    merged = pd.merge(recipe_df, ingredient_price_df, on="ingredient", how="left")
    merged["ingredient_cost"] = merged["qty_per_unit"] * merged["cost_per_unit"]

    dish_cost = merged.groupby("item_name")["ingredient_cost"].sum().reset_index()
    dish_cost.rename(columns={"ingredient_cost": "total_cost"}, inplace=True)

    margin_df = pd.merge(dish_cost, menu_df, on="item_name")
    margin_df["profit"] = margin_df["selling_price"] - margin_df["total_cost"]
    margin_df["margin_%"] = (margin_df["profit"] / margin_df["selling_price"] * 100).round(2)

    margin_df = pd.merge(margin_df, sales_df, on="item_name", how="left")

    recommendations = []

    for _, row in margin_df.iterrows():
        item = row['item_name']
        margin = row['margin_%']
        total_sales = row['total_sales']
        ingredients = recipe_df[recipe_df["item_name"] == item]["ingredient"].tolist()

        increase_count = 0
        for ing in ingredients:
            match = trend_df[trend_df["ingredient"] == ing]
            if not match.empty:
                old = match["last_month_cost"].values[0]
                new = match["current_cost"].values[0]
                if (new - old) / old > 0.1:
                    increase_count += 1

        if increase_count >= 1 and margin < 25:
            recommendations.append(f"⬆️ Increase price of '{item}' (cost ↑, margin low)")
        elif total_sales > 100 and margin > 30:
            recommendations.append(f"⬆️ Increase price of '{item}' (high demand & margin)")
        elif total_sales < 50 and margin > 40:
            recommendations.append(f"⬇️ Consider reducing price of '{item}' (low demand, high margin)")

    if not recommendations:
        return "All prices are optimal. No action needed."

    return "📈 Dynamic Pricing Suggestions:\n" + "\n".join(recommendations)
