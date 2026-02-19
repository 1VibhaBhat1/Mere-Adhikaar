import streamlit as st
import anthropic
import os

st.set_page_config(page_title="Mere Adhikaar", page_icon="⚖️")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("⚖️ Mere Adhikaar")
st.caption("Know Your Rights in Your Language")

# Sidebar
with st.sidebar:
    st.header("🆘 Emergency")
    st.markdown("**112** - Emergency")
    st.markdown("**181** - Women's Helpline")
    st.markdown("**100** - Police")
    
    st.header("📞 Legal Aid")
    st.markdown("**NALSA:** 011-23382778")
    st.markdown("[Panel Lawyers](https://nalsa.gov.in/panel-lawyers/)")

# Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
            )
            
            answer = response.content[0].text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
