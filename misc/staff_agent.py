from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.staff_forecast import upcoming_staff_schedule_text

llm = ChatOpenAI(temperature=0)
staff_tool = Tool(
    name="StaffShiftForecaster",
    func=upcoming_staff_schedule_text,
    description="Forecast the number of staff needed for lunch and dinner."
)

staff_agent = initialize_agent(
    tools=[staff_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
