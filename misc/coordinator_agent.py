# agent/coordinator_agent.py

from tools.reorder        import reorder_summary_text
from tools.sentiment      import summarize_sentiment_trends
from tools.staff_forecast import upcoming_staff_schedule_text
from tools.pricing        import dynamic_price_recommendation
from tools.profitability  import low_margin_dishes
from tools.promo          import promo_summary_text
from tools.supplier       import supplier_performance_summary

# 1️⃣ Build a mapping from “intent” to your raw‐text function
TOOL_MAP = {
    "reorder":   reorder_summary_text,
    "sentiment": summarize_sentiment_trends,
    "staff":     upcoming_staff_schedule_text,
    "pricing":   dynamic_price_recommendation,
    "profit":    low_margin_dishes,
    "promo":     promo_summary_text,
    "supplier":  supplier_performance_summary,
}

# 2️⃣ Simple router: pick the right key from the user question
def route_agent(question: str) -> str:
    q = question.lower()
    if "reorder" in q:               
        return "reorder"
    if "review" in q or "complaint" in q: 
        return "sentiment"
    if "staff" in q:                 
        return "staff"
    if "price" in q:                 
        return "pricing"
    if "profit" in q or "margin" in q:    
        return "profit"
    if "promo" in q:                 
        return "promo"
    if "supplier" in q:              
        return "supplier"
    return "reorder"  # fallback

# 3️⃣ One‑call entrypoint for your Streamlit app
def run_agent_graph(user_question: str) -> str:
    key = route_agent(user_question)
    func = TOOL_MAP[key]
    # All of your tool functions already return a plain string
    return func()
