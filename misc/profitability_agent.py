from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.profitability import low_margin_dishes

llm = ChatOpenAI(temperature=0)
profitability_tool = Tool(
    name="DishProfitabilityChecker",
    func=low_margin_dishes,
    description="List dishes with low profit margins based on ingredient costs."
)

profitability_agent = initialize_agent(
    tools=[profitability_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
