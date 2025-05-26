from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.pricing import dynamic_price_recommendation

llm = ChatOpenAI(temperature=0)
pricing_tool = Tool(
    name="PriceOptimizer",
    func=dynamic_price_recommendation,
    description="Recommend price changes based on demand and cost trends."
)

pricing_agent = initialize_agent(
    tools=[pricing_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
