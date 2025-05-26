from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.supplier import supplier_performance_summary

llm = ChatOpenAI(temperature=0)
supplier_tool = Tool(
    name="SupplierPerformanceTracker",
    func=supplier_performance_summary,
    description="Evaluate supplier reliability and pricing consistency."
)

supplier_agent = initialize_agent(
    tools=[supplier_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
