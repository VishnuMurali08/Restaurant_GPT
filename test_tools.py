from tools.reorder import reorder_summary_text
from tools.profitability import low_margin_dishes
from tools.staff_forecast import upcoming_staff_schedule_text
from tools.sentiment import summarize_sentiment_trends
from tools.pricing import dynamic_price_recommendation
from tools.promo import promo_summary_text
from tools.supplier import supplier_performance_summary


print("=== 📦 Reorder Suggestion ===")
print(reorder_summary_text())

print("\n=== 💸 Low Margin Dishes ===")
print(low_margin_dishes())

print("\n=== 👨‍🍳 Staff Forecast ===")
print(upcoming_staff_schedule_text())

print("\n=== 💬 Sentiment Summary ===")
print(summarize_sentiment_trends())

print("\n=== 💹 Pricing Suggestion ===")
print(dynamic_price_recommendation())

print("\n=== 📣 Promo Effectiveness ===")
print(promo_summary_text())

print("\n=== 🚚 Supplier Performance ===")
print(supplier_performance_summary())


