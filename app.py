import streamlit as st
from agent.langchain_agent import restaurant_agent
from agent.prompt_chain import prompt_chain

st.set_page_config(page_title="Restaurant Data GPT", layout="centered")
st.title("🍽️ Restaurant Data GPT")
st.subheader("Ask your restaurant in plain English")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Capture user input
user_input = st.chat_input("e.g., What stock should I reorder?")

if user_input:
    with st.spinner("🤖 Thinking..."):
        try:
            # 1️⃣ Run your LangChain Conversational Agent
            raw_response = restaurant_agent.invoke(user_input)
        except Exception as e:
            raw_response = f"⚠️ Agent error:\n{e}"

        # 2️⃣ Post‑process with your Prompt Chain for a friendly polish
        try:
            improved = prompt_chain.invoke({
                "user_question": user_input,
                "raw_answer": raw_response
            })
        except Exception:
            # Fallback to raw if prompt_chain fails
            improved = raw_response

        # Store both turns
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", improved))

# Render the conversation
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
