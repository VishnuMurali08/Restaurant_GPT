# agent/langchain_agent.py

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from tools.reorder import reorder_summary_text
from tools.profitability import low_margin_dishes
from tools.staff_forecast import upcoming_staff_schedule_text
from tools.sentiment import summarize_sentiment_trends
from tools.pricing import dynamic_price_recommendation
from tools.promo import promo_summary_text
from tools.supplier import supplier_performance_summary

# Create LangChain Tools
TOOLS = [
    Tool(
        name="SmartInventoryReorder",
        func=reorder_summary_text,
        description="Suggest items to reorder based on stock and forecasted demand."
    ),
    Tool(
    name="DishProfitabilityChecker",
    func=low_margin_dishes,
    description="""
        List dishes with low profit margins based on ingredient costs.
        This tool analyzes ingredient costs and selling prices to find items with margin below 30%.
        You can also specify another threshold like 'below 25% margin'.
        Example queries: 'Which dishes are not profitable?', 'Show dishes below 40% margin'.
    """ 
    ),
    Tool(
        name="StaffShiftForecaster",
        func=upcoming_staff_schedule_text,
        description="Forecast the number of staff needed for lunch and dinner."
    ),
    Tool(
        name="ReviewSentimentAnalyzer",
        func=summarize_sentiment_trends,
        description="Summarize real customer complaints for any theme: 'Service', 'Food Quality', 'Waiting Time', 'Price', or 'None'."
    ),
    Tool(
        name="PriceOptimizer",
        func=dynamic_price_recommendation,
        description="Recommend price changes based on demand and cost trends."
    ),
    Tool(
        name="PromoEffectivenessAnalyzer",
        func=promo_summary_text,
        description="Evaluate marketing promotion success."
    ),
    Tool(
        name="SupplierPerformanceTracker",
        func=supplier_performance_summary,
        description="Evaluate supplier reliability and pricing consistency."
    )
]

# Setup Chat Agent
llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

restaurant_agent = initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
