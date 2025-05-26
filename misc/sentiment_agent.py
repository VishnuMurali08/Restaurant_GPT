from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from tools.sentiment import summarize_sentiment_trends

llm = ChatOpenAI(temperature=0)
sentiment_tool = Tool(
    name="ReviewSentimentAnalyzer",
    func=summarize_sentiment_trends,
    description="Analyze review sentiments and complaint themes."
)

sentiment_agent = initialize_agent(
    tools=[sentiment_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)
