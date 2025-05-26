from prophet import Prophet
import pandas as pd
from data.db import fetch_table


def forecast_item_demand(sales_df, item_name, days=7):
    df = sales_df[sales_df["item_name"] == item_name]
    df_grouped = df.groupby("sale_date")["quantity"].sum().reset_index()
    df_grouped.rename(columns={"sale_date": "ds", "quantity": "y"}, inplace=True)

    model = Prophet()
    model.fit(df_grouped)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(days)


def generate_reorder_recommendations():
    sales_df = fetch_table("sales_data")
    inventory_df = fetch_table("inventory_data")
    recommendations = []

    for _, row in inventory_df.iterrows():
        item = row['item_name']
        stock = row['current_stock']
        threshold = row['restock_threshold']
        lead_time = row['lead_time_days']

        forecast_df = forecast_item_demand(sales_df, item, days=lead_time)
        predicted_demand = forecast_df['yhat'].sum()

        if stock - predicted_demand <= threshold:
            recommendations.append({
                "item_name": item,
                "predicted_demand": int(predicted_demand),
                "current_stock": stock,
                "restock_threshold": threshold,
                "suggested_order_qty": int(predicted_demand + threshold - stock),
                "lead_time_days": lead_time
            })

    return pd.DataFrame(recommendations)


#def reorder_summary_text():
def reorder_summary_text(_=None):
    df = generate_reorder_recommendations()
    if df.empty:
        return "All inventory levels are sufficient. No reorders needed."

    text = "\U0001F4E6 Reorder Suggestions:\n"
    for _, row in df.iterrows():
        text += (
            f"- {row['item_name']}: Order {row['suggested_order_qty']} units "
            f"(Forecasted demand: {row['predicted_demand']}, "
            f"Current stock: {row['current_stock']})\n"
        )
    return text