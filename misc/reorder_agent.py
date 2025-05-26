from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.reorder import reorder_summary_text

llm = ChatOpenAI(temperature=0)
reorder_tool = Tool(
    name="SmartInventoryReorder",
    func=reorder_summary_text,
    description="Suggest items to reorder based on stock and forecasted demand."
)

reorder_agent = initialize_agent(
    tools=[reorder_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
