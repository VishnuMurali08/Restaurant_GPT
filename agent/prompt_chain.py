from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# === Friendly Rewrites for All Tools ===
examples = [
    # 🔁 reorder_summary_text
    {
        "user_question": "Which stock should I reorder?",
        "raw_answer": """📦 Reorder Suggestions:
- Grilled Salmon: Order 4 units (Forecasted demand: 24, Current stock: 30)
- Chicken Wings: Order 10 units (Forecasted demand: 45, Current stock: 20)""",
        "rewritten": """Hey there! 🌟 Based on our **SmartInventoryReorder** tool, here are the items to consider restocking:

- 🐟 **Grilled Salmon** → Order 4 units  
  _(📈 Demand: 24, 📦 Stock: 30)_

- 🍗 **Chicken Wings** → Order 10 units  
  _(📈 Demand: 45, 📦 Stock: 20)_

Let me know if you want to place the orders! 🛒"""
    },

    # 💸 low_margin_dishes
    {
        "user_question": "Which dishes have low profit margin?",
        "raw_answer": """⚠️ Dishes with Low Profit Margin (below 30%):
- Spaghetti Bolognese: 21.5% margin (Cost: $5.60, Price: $7.15)
- Chicken Kebab: 19.8% margin (Cost: $4.80, Price: $6.00)""",
        "rewritten": """Heads up! 📉 The following dishes have lower-than-ideal profit margins:

- 🍝 **Spaghetti Bolognese** – 21.5%  
  _(Cost: $5.60, Price: $7.15)_

- 🍢 **Chicken Kebab** – 19.8%  
  _(Cost: $4.80, Price: $6.00)_

You might want to review pricing or recipe costs! 💰"""
    },

    # 👨‍🍳 upcoming_staff_schedule_text
    {
        "user_question": "What's the staff schedule for next week?",
        "raw_answer": """🧑‍🍳 Recommended Staff Schedule (Next 7 Days):
2024-06-15: Lunch - 3 | Dinner - 5
2024-06-16: Lunch - 2 | Dinner - 4""",
        "rewritten": """Hi there! 👋 Here's the staffing forecast for the upcoming week:

- 📅 **June 15**  
  🍽️ Lunch: 3 staff  
  🌆 Dinner: 5 staff

- 📅 **June 16**  
  🍽️ Lunch: 2 staff  
  🌆 Dinner: 4 staff

Let me know if you'd like to adjust the shifts!"""
    },

    # 🗣️ summarize_sentiment_trends
    {
        "user_question": "What are customers saying in reviews?",
        "raw_answer": """📊 **Overall Sentiment Summary:**
- Positive: 120
- Negative: 45
- Neutral: 30

⚠️ **Overall Complaint Themes:**
- Service: 20
- Food Quality: 15
- Waiting Time: 10""",
        "rewritten": """Here’s what customers have been saying lately! 🗣️

### 💬 Sentiment Summary
- 😊 Positive: 120  
- 😐 Neutral: 30  
- 😞 Negative: 45  

### ⚠️ Most Common Complaints
- 🧑‍💼 Service: 20  
- 🍽️ Food Quality: 15  
- ⏳ Waiting Time: 10"""
    },

    # 📈 dynamic_price_recommendation
    {
        "user_question": "Do we need to adjust any menu prices?",
        "raw_answer": """📈 Dynamic Pricing Suggestions:
⬆️ Increase price of 'Pasta' (cost ↑, margin low)
⬇️ Consider reducing price of 'Deluxe Burger' (low demand, high margin)""",
        "rewritten": """Sure thing! Here's what our pricing tool recommends:

- 🔺 **Pasta** – Price increase suggested due to rising costs and low margin  
- 🔻 **Deluxe Burger** – Consider reducing price due to low demand despite high margin

Let me know if you want help adjusting the prices! 💸"""
    },

    # 📣 promo_summary_text
    {
        "user_question": "How effective were the latest promotions?",
        "raw_answer": """📣 Promo Effectiveness:
- Summer Special (Burger via Instagram): 25.5% uplift in sales (Before: 200, During: 251)""",
        "rewritten": """Here's how your recent promo performed! 📣

- 🍔 **Summer Special** (Burger via Instagram):  
  🔼 **25.5% sales uplift**  
  _(Before: 200, During: 251)_

Great job on the campaign! 🎯"""
    },

    # 🚚 supplier_performance_summary
    {
        "user_question": "Which suppliers are reliable?",
        "raw_answer": """🚚 Supplier Performance:
- FreshMeats: 5.5% late deliveries, Avg Price = $4.20, Volatility = ±$0.25""",
        "rewritten": """Here’s a snapshot of supplier performance: 📦

- 🏢 **FreshMeats**  
  ⏱️ Late Deliveries: 5.5%  
  💰 Avg Price: $4.20  
  📉 Price Volatility: ±$0.25

Looks like they're pretty reliable! ✅"""
    }
]

# === Prompt Template for Each Example ===
example_prompt = PromptTemplate(
    input_variables=["user_question", "raw_answer", "rewritten"],
    template="""
User asked: "{user_question}"  
System said: "{raw_answer}"  
Rewritten response:  
{rewritten}
"""
)

# === Few-Shot Prompt ===
prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="""
Now rewrite the following system response to be:
- Friendly and conversational (like a helpful restaurant assistant)
- Use emojis to enhance understanding
- Retain important numbers and names (like prices, margins, dates)
- Format clearly using markdown when helpful
- Keep it concise, human, and easy to understand

User asked: "{user_question}"  
System said: "{raw_answer}"  

Rewritten response:
""",
    input_variables=["user_question", "raw_answer"]
)

# === LLM Chain ===
llm = ChatOpenAI(temperature=0.6)  # Friendly tone
prompt_chain = prompt_template | llm
