# agent/prompt_chain.py
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI  

prompt_template = PromptTemplate(
    input_variables=["user_question", "raw_answer"],
    template="""
You're a helpful restaurant assistant AI.

The user asked: "{user_question}"

The system generated this answer: "{raw_answer}"

Please rewrite this response to:
- Be clear, friendly, and conversational
- Add emojis where suitable
- Format using markdown
- Organize lists or numbers well
- Keep it concise but informative

Rewritten response:
"""
)

llm = ChatOpenAI(temperature=0.5)
# prompt_chain = LLMChain(llm=llm, prompt=prompt_template)
prompt_chain = prompt_template | llm
