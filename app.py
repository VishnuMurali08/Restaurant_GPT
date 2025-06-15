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
        # Step 1: LangChain Agent response
        try:
            raw_response = restaurant_agent.invoke(user_input)

            # Extract meaningful text
            if isinstance(raw_response, dict) and "output" in raw_response:
                raw_text = raw_response["output"]
            elif hasattr(raw_response, "content"):
                raw_text = raw_response.content
            else:
                raw_text = str(raw_response)

        except Exception as e:
            raw_text = f"⚠️ Agent error:\n{e}"

        # Step 2: Prompt chain to rewrite
        try:
            polished = prompt_chain.invoke({
                "user_question": user_input,
                "raw_answer": raw_text
            })

            # ✅ Extract only the final string content
            if hasattr(polished, "content"):
                final_response = polished.content
            elif isinstance(polished, dict) and "output" in polished:
                final_response = polished["output"]
            else:
                final_response = str(polished)

        except Exception as e:
            final_response = raw_text
            st.error(f"⚠️ Prompt chain error: {e}")

        # Step 3: Store messages
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", final_response))

# Display chat history
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
