# tools/staff_forecast.py

import pandas as pd
from prophet import Prophet
from data.db import fetch_table


def forecast_staff_needs(days=7):
    sales_df = fetch_table("sales_data")
    df = sales_df.groupby("sale_date")["quantity"].sum().reset_index()
    df.rename(columns={"sale_date": "ds", "quantity": "y"}, inplace=True)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    forecast = forecast[["ds", "yhat"]].tail(days)

    staff_recommendations = []
    for _, row in forecast.iterrows():
        lunch_orders = row["yhat"] * 0.45
        dinner_orders = row["yhat"] * 0.55
        lunch_staff = int(round(lunch_orders / 10))
        dinner_staff = int(round(dinner_orders / 7))

        staff_recommendations.append({
            "date": row["ds"].date(),
            "lunch_staff": lunch_staff,
            "dinner_staff": dinner_staff
        })

    return pd.DataFrame(staff_recommendations)


# def upcoming_staff_schedule_text():
def upcoming_staff_schedule_text(_=None):
    df = forecast_staff_needs(days=7)
    text = "\U0001f9d1\u200d\U0001f373 Recommended Staff Schedule (Next 7 Days):\n"
    for _, row in df.iterrows():
        text += (
            f"{row['date']}: Lunch - {row['lunch_staff']} | Dinner - {row['dinner_staff']}\n"
        )
    return text