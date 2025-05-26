from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.promo import promo_summary_text

llm = ChatOpenAI(temperature=0)
promo_tool = Tool(
    name="PromoEffectivenessAnalyzer",
    func=promo_summary_text,
    description="Evaluate marketing promotion success."
)

promo_agent = initialize_agent(
    tools=[promo_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
